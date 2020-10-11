import discord
from discord.ext import commands
import os
import sys
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import checks
from git import Repo, Remote


def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    # remove `foo`
    return content.strip('` \n')


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.file = "admin"
        self._last_result = None

    @commands.group(name='admin', hidden=True)
    @commands.check(checks.is_bot_admin)
    async def main_msg(self, ctx: commands.Context):
        """Commands reserved for administrators of Fish-Bot"""
        if ctx.subcommand_passed is None:
            text = "List of commands :"
            for cmd in sorted(self.main_msg.commands, key=lambda x: x.name):
                text += "\n- {} *({})*".format(cmd.name,
                                               '...' if cmd.help is None else cmd.help.split('\n')[0])
                if type(cmd) == commands.core.Group:
                    for cmds in cmd.commands:
                        text += "\n        - {} *({})*".format(
                            cmds.name, cmds.help.split('\n')[0])
            await ctx.send(text)

    @main_msg.command(name='pull', hidden=True)
    async def gitpull(self, ctx: commands.Context):
        """Pull from Github"""
        m = await ctx.send("Pulling from GitHub...")
        repo = Repo(os.getcwd())
        assert not repo.bare
        origin = repo.remotes.origin
        origin.pull()
        await self.restart_bot(ctx)

    @main_msg.command(name='shutdown')
    async def shutdown(self, ctx: commands.Context):
        """Eteint le bot"""
        m = await ctx.send("Cleaning up...")
        await self.cleanup_workspace()
        await m.edit(content="Shutting down...")
        await self.bot.change_presence(status=discord.Status('offline'))
        self.bot.log.info("Bot Shut Down")
        await self.bot.logout()
        await self.bot.close()

    async def cleanup_workspace(self):
        for folderName, _, filenames in os.walk('.'):
            for filename in filenames:
                if filename.endswith('.pyc'):
                    os.unlink(folderName+'/'+filename)
            if folderName.endswith('__pycache__'):
                os.rmdir(folderName)

    @main_msg.command(name='reboot')
    async def restart_bot(self, ctx: commands.Context):
        """Relance le bot"""
        await ctx.send(content="Rebooting bot...")
        await self.cleanup_workspace()
        self.bot.log.info("Rebooting bot...")
        sys.argv.append('beta' if self.bot.beta else 'stable')
        os.execl(sys.executable, sys.executable, *sys.argv)

    @main_msg.command(name='purge')
    @commands.guild_only()
    async def clean(self, ctx: commands.Context, limit: int):
        """Remove <x> messages"""
        if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            await ctx.send("I can\'t manage messages!")
        elif not ctx.channel.permissions_for(ctx.guild.me).read_message_history:
            await ctx.send("I can\'t see the history of messages!")
        else:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit)
            await ctx.send('{} messages removed !'.format(len(deleted)), delete_after=3.0)

    @main_msg.command(name='reload')
    async def reload_cog(self, ctx: commands.Context, *, cog: str):
        """Reload a module"""
        cogs = cog.split(" ")
        errors_cog = self.bot.get_cog("Errors")
        if len(cogs) == 1 and cogs[0] == 'all':
            cogs = sorted([x.file for x in self.bot.cogs.values()])
        reloaded_cogs = list()
        for cog in cogs:
            try:
                self.bot.reload_extension("plugins."+cog)
            except ModuleNotFoundError:
                await ctx.send("Cog {} can't be found".format(cog))
            except commands.errors.ExtensionNotLoaded:
                await ctx.send("Cog {} was never loaded".format(cog))
            except Exception as e:
                await errors_cog.on_error(e, ctx)
                await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                self.bot.log.info("Module {} reloaded".format(cog))
                reloaded_cogs.append(cog)
        if len(reloaded_cogs) > 0:
            await ctx.bot.get_cog("General").count_lines_code()
            await ctx.send("These cogs has successfully reloaded: {}".format(", ".join(reloaded_cogs)))

    @main_msg.command(name="add_cog", hidden=True)
    async def add_cog(self, ctx: commands.Context, name: str):
        """Add a cog to the bot"""
        try:
            self.bot.load_extension("plugins."+name)
            await ctx.send("Module '{}' added !".format(name))
            self.bot.log.info("Module {} added".format(name))
        except Exception as e:
            await ctx.send(str(e))

    @main_msg.command(name="del_cog", aliases=['remove_cog'], hidden=True)
    async def rm_cog(self, ctx: commands.Context, name: str):
        """Remove a cog from the bot"""
        try:
            self.bot.unload_extension("plugins."+name)
            await ctx.send("Module '{}' deactivated !".format(name))
            self.bot.log.info("Module {} deactivated".format(name))
        except Exception as e:
            await ctx.send(str(e))

    @main_msg.command(name="cogs", hidden=True)
    async def cogs_list(self, ctx: commands.Context):
        """See list of cogs"""
        text = str()
        for k, v in self.bot.cogs.items():
            text += "- {} ({}) \n".format(v.file, k)
        await ctx.send(text)

    @main_msg.command(name="activity")
    async def change_activity(self, ctx: commands.Context, Type: str, * act: str):
        """Change bot activity"""
        act = " ".join(act)
        if Type in ['game', 'play', 'playing']:
            await self.bot.change_presence(activity=discord.Game(name=act))
        elif Type in ['watch', 'see', 'watching']:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=act))
        elif Type in ['listen', 'listening']:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=act))
        elif Type in ['stream']:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=act))
        else:
            await ctx.send("Select *play*, *watch*, *listen* ou *stream*")
        await ctx.message.delete()

    @main_msg.command(name='eval')
    @commands.check(checks.is_bot_admin)
    async def _eval(self, ctx: commands.Context, *, body: str):
        """Evaluates a code
        Credits: Rapptz (https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py)"""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }
        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        try:
            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        except Exception as e:
            await self.bot.get_cog('Errors').on_error(e, ctx)
            return
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    bot.add_cog(Admin(bot))
