import discord
from discord.ext import commands
import checks
import asyncio
import time, random
import sys
import psutil
import os
from discord.ext import tasks

class LinkUsernames(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.file = "linkusernames"
        self._last_result = None
        self.usernames = dict()
        self.db_get_usernames()

    def db_get_usernames(self):
        c = self.bot.database.cursor()
        for row in c.execute('SELECT * FROM usernames'):
            self.usernames[row[1]] = row[2]
        c.close()

    def db_add_username(self, user: discord.Member, ign: str):
        c = self.bot.database.cursor()
        c.execute(f"INSERT or IGNORE INTO usernames (guild, discordid, ign) VALUES (?, ?, ?)", (602313280702382106, user.id, ign))
        self.usernames[id] = ign
        self.bot.database.commit()

    def db_query_ign(self, ign: str):
        c = self.bot.database.cursor()
        for row in c.execute('SELECT * FROM usernames WHERE ign=\'' + ign + '\';'):
            if row:
                return row[1]
            else:
                return False

    def db_query_d(self, id: str):
        c = self.bot.database.cursor()
        for row in c.execute('SELECT * FROM usernames WHERE discordid=\'' + str(id) + '\';'):
            if row:
                return row[2]
            else:
                return False

    @commands.command(name='link')
    async def link(self, ctx: commands.Context, ign: str):
        """Link your discord username to your IGN"""
        self.db_add_username(ctx.author, ign)
        await ctx.send("Done! Added " + ctx.author.name + "#" + ctx.author.discriminator + " as " + ign)

    @commands.command(name='whoign')
    async def whoisign(self, ctx: commands.Context, ign: str):
        """Lookup who a user is from IGN"""
        id = self.db_query_ign(ign)
        if id:
            for guild in self.bot.guilds:
                for member in guild.members:
                    if member.id == id:
                        themember = member
                        await ctx.send("Member: " + member.name + "#" + member.discriminator)
        else:
            await ctx.send("No member found!")

    @commands.command(name='whod')
    async def whod(self, ctx: commands.Context):
        id = ctx.message.mentions[0].id
        ign = self.db_query_d(id)
        if ign:
            await ctx.send("IGN: " + ign)
        else:
            await ctx.send("Not found!")

def setup(bot):
    bot.add_cog(LinkUsernames(bot))
