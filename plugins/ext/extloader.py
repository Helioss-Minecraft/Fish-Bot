import discord
import string
import requests
from pathlib import Path
from discord.ext import commands



class ExtLoader(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.file = "extloader"
        self._last_result = None

        self.path = "./plugins/ext/"
        extp = Path(self.path)

        if not extp.exists:
            extp.mkdir()

    @commands.group(name="ext")
    @commands.check(checks.is_staff)
    async def ext_group(self, ctx: commands.Context):
        if ctx.invoked_subcommand == None:
            await ctx.send("Invalid usage. Please provide a subcommand.")

    @ext_group.command(name="new")
    async def ext_new(self, ctx: commands.Context, name: str = None):
        if len(ctx.message.attachments) != 1:
            await ctx.send("You must attach a file.")
            return

        a = ctx.message.attachments[0]
        name = name if name else a.filename

        if name.split('.')[1] != 'py':
            await ctx.send("Filename must end in .py")
            return

        url = a.url

        with Path(f"{self.path}{name}").open('w') as f:
            content = requests.get(url).content.decode("utf-8")
            f.write(content)

        try:
            self.bot.load_extension(f"extensions.{name.strip('.py')}")
            await ctx.send(f"New cog {name} created and loaded.")
        except:
            await ctx.send(f"Created new cog {name} but loading failed.")


def setup(bot):
    bot.add_cog(ExtLoader(bot))
