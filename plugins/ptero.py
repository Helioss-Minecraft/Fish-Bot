import discord
from discord.ext import commands
import checks
import asyncio
import time
import sys
import psutil
import os
from platform import system as system_name  # Returns the system/OS name
from subprocess import call as system_call  # Execute a shell command
import nbtlib
import utils, os
from nbtlib import Compound, Byte, String, Short, Int, Double

class Ptero(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.file = "ptero"
        self._last_result = None


    @commands.group(name='ptero', hidden=True)
    @commands.check(checks.is_staff)
    async def main_msg(self, ctx: commands.Context):
        """Pterodactyl-Related commands"""
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
    @main_msg.command(name='resetcoords')
    async def resetcoords(self, ctx: commands.Context, node: str, server: str, player: str, x: int, y: int, z: int, dim: int):
        """Reset a player's coords"""
        await ctx.send("Resetting player " + player + " to coords: " + str(x) + ", " + str(y) + ", " + str(z) + " " + "in dimension " + str(dim) + "...")
        if node == "london":
            serverid = utils.londonids[server]
        elif args == "canada":
            serverid = utils.canadaids[server]
        elif args == "germany":
            serverid = utils.germanyids[server]
        uuid = utils.getUUID(player)
        if uuid:
            url = serverid + "/world/playerdata/" + uuid + ".dat"
            print("Downloading " + url + "...")
            utils.download(url, uuid + ".dat", node)
            dir_path = cwd = os.getcwd()
            nbtfile = nbtlib.load(dir_path + "/" + uuid + ".dat")
            print("Resetting " + player + "\'s coordinates to " + str(x) + "," + str(y) + "," + str(z) + "...")
            nbtfile.root["Pos"][0] = x
            nbtfile.root["Pos"][1] = y
            nbtfile.root["Pos"][2] = z
            nbtfile.root["Dimension"] = Int(dim)
            nbtfile.save()
            print("Uploading to server...")
            utils.upload(dir_path + "/" + uuid + ".dat", serverid + "/world/playerdata/" + uuid + ".dat", node)
            print("Uploaded!")
            os.unlink(dir_path + "/" + uuid + ".dat")
        await ctx.send("Done!")

    @main_msg.command(name='resetspawn')
    async def resetspawn(self, ctx: commands.Context, node: str, server: str, username: str):
        await ctx.send("Resetting player " + username + " to spawn...")
        if node == "london":
            serverid = utils.londonids[server]
        elif node == "canada":
            serverid = utils.canadaids[server]
        elif node == "germany":
            serverid = utils.germanyids[server]
        uuid = utils.getUUID(username)
        if uuid:
            if not os.path.exists(uuid + ".dat"):
                url = serverid + "/world/playerdata/" + uuid + ".dat"
                print(("Downloading " + url + "..."))
                utils.download(url, uuid + ".dat", node)
            dir_path = os.getcwd()
            nbtfile = nbtlib.load(dir_path + "/" + uuid + ".dat")

            url = serverid + "/world/level.dat"

            print(("Downloading " + url + "..."))
            utils.download(url, "level.dat", node)
            worldfile = nbtlib.load(dir_path + "/" + "level.dat")
            xCoord = worldfile.root["Data"]["SpawnX"]
            yCoord = worldfile.root["Data"]["SpawnY"]
            zCoord = worldfile.root["Data"]["SpawnZ"]

            print(("Resetting " + username + "\'s coordinates to " + str(xCoord) + "," + str(yCoord) + "," + str(zCoord) + "..."))
            nbtfile.root["Pos"][0] = Double(xCoord)
            nbtfile.root["Pos"][1] = Double(yCoord)
            nbtfile.root["Pos"][2] = Double(zCoord)
            nbtfile.root["Dimension"] = Int(0)
            nbtfile.save()
            print("Uploading to server...")
            utils.upload(dir_path + "/" + uuid + ".dat", serverid + "/world/playerdata/" + uuid + ".dat", node)
            print("Uploaded!")
            os.unlink(dir_path + "/" + uuid + ".dat")
            os.unlink(dir_path + "/" + "level.dat")
            await ctx.send("Done!")

def setup(bot):
    bot.add_cog(Ptero(bot))
