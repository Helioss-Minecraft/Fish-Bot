import argparse
import nbtlib
import utils, os
from utils import *
from nbtlib import Compound, Byte, String, Short, Double, Int

def checkNode(value):
    strvalue = str(value)
    if strvalue.lower() not in ["london", "canada", "germany"]:
        raise argparse.ArgumentTypeError("%s is an invalid value!" % value)
    return strvalue

def checkServer(value):
    strvalue = str(value)
    if strvalue not in utils.ids.keys():
        raise argparse.ArgumentTypeError("%s is an invalid value!" % value)
    return strvalue


parser = argparse.ArgumentParser(description='Edit the position of the player.')
parser.add_argument("node", nargs=1, type=checkNode)
parser.add_argument("server", nargs=1, type=checkServer)
parser.add_argument("player", nargs=1, type=str)
args = parser.parse_args()

server = args.server[0]
node = args.node[0]
username = args.player[0]

if node == "london":
    serverid = londonids[server]
elif node == "canada":
    serverid = canadaids[server]
elif node == "germany":
    serverid = germanyids[server]
uuid = getUUID(username)
if uuid:
    if not os.path.exists(uuid + ".dat"):
        url = serverid + "/world/playerdata/" + uuid + ".dat"
        print(("Downloading " + url + "..."))
        download(url, uuid + ".dat", node)
    dir_path = cwd = os.getcwd()
    nbtfile = nbtlib.load(dir_path + "/" + uuid + ".dat")

    url = serverid + "/world/level.dat"

    print(("Downloading " + url + "..."))
    download(url, "level.dat", node)
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
    upload(dir_path + "/" + uuid + ".dat", serverid + "/world/playerdata/" + uuid + ".dat", node)
    print("Uploaded!")
    os.unlink(dir_path + "/" + uuid + ".dat")
    os.unlink(dir_path + "/" + "level.dat")
