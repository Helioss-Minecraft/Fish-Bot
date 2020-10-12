import discord
from discord.ext import commands
import checks
import asyncio
import time, random
import sys
import psutil
import os
from discord.ext import tasks

class NickAspiring(commands.Cog):

    nicknames = ("Polypropylene",
                         "Polyvinyl-Chloride",
                         "Polyvinylidenechloride",
                         "Polyacrylonitrile",
                         "Polytetrafluoroethylene",
                         "Polymethylmethacrylate",
                         "Polyvinylacetate",
                         "Cis-Polyisoprene",
                         "Polychloroprene",
                         "Polyurethane",
                         "Polybenzimidazole",
                         "Polyacetal",
                         "Polyacrylonitrile",
                         "Polybutadiene",
                         "Polybutylene-Terephthalate",
                         "Polycaprolactam",
                         "Polycaprolactam",
                         "Polychlorotrifluoroethylene",
                         "Polycyclohexyl-Methacrylate",
                         "Polycopractom",
                         "Polydimethylsiloxane",
                         "Polydodecano-12-Lactam",
                         "Polyether-Ether-Ketone",
                         "Polyether-Ketone-Ketone",
                         "Polyethersulfone",
                         "Polyethyl-Acrylate",
                         "Polyethylene-Glycol",
                         "Polyethylene-Naphthalate",
                         "Polyethylene-terephthalate)",
                         "Polyhexamethylene-Adipamide",)

    def __init__(self, bot):
        self.bot = bot
        self.file = "nickaspiring"
        self._last_result = None


    @tasks.loop(hours=4)
    async def nick(self):
        member = self.bot.get_user("642430396683911187")
        member.edit(nick="Aspiring " + nicknames[random.randint(0, len(nicknames) - 1)])

def setup(bot):
    bot.add_cog(NickAspiring(bot))
