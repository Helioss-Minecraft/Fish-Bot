import argparse
import nbtlib
import utils, os
from nbtlib import Compound, Byte, String, Short

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
parser.add_argument("xCoord", nargs=1, type=float)
parser.add_argument("yCoord", nargs=1, type=float)
parser.add_argument("zCoord", nargs=1, type=float)
args = parser.parse_args()

if args.node[0] == "london":
    serverid = utils.londonids[args.server[0]]
elif args.node[0] == "canada":
    serverid = utils.canadaids[args.server[0]]
elif args.node[0] == "germany":
    serverid = utils.germanyids[args.server[0]]
uuid = utils.getUUID(args.player[0])
if uuid:
    url = serverid + "/world/playerdata/" + uuid + ".dat"
    print("Downloading " + url + "...")
    utils.download(url, uuid + ".dat", args.node[0])
    dir_path = cwd = os.getcwd()
    nbtfile = nbtlib.load(dir_path + "/" + uuid + ".dat")
    print("Resetting " + args.player[0] + "\'s coordinates to " + str(args.xCoord[0]) + "," + str(args.yCoord[0]) + "," + str(args.zCoord[0]) + "...")
    nbtfile.root["Pos"][0] = args.xCoord[0]
    nbtfile.root["Pos"][1] = args.yCoord[0]
    nbtfile.root["Pos"][2] = args.zCoord[0]
    nbtfile.save()
    print("Uploading to server...")
    utils.upload(dir_path + "/" + uuid + ".dat", serverid + "/world/playerdata/" + uuid + ".dat", args.node[0])
    print("Uploaded!")
    os.unlink(dir_path + "/" + uuid + ".dat")
