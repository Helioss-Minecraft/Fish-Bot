import requests, os, sys
import json, bs4, re, datetime

nodes = {
    "london": "http://ovh.helioss.co:1111/",
    "canada": "http://cana.helioss.co:1111/",
    "germany": "http://newgermany.helioss.co:39916/"
}

auths = ('6b9164e2052e92c2c9e049da66c423e1781a55086f9b00e3a1f9f0bc04df846f26dae0a037c74ea1d9c6f68ed0906d9807a7a97a49b37610baacd89542cda2f0', 'c289ee0bf6ac91fc19b603f8ccc9459ff2ee5baf5cfc0cc2db985fa4ac87357c44aa70fc8b9a9276e6f7228b135f32d68840185111bedd31f5c4b52bf3fb0a31')

londonids = {
    "OmniEU": "c109582e-dc78-4a24-b256-630afca1b88c",
    "PO3Titan": "6d8aa79c-a242-488a-b099-f018ec3749a4",
    "MCE": "3fa2f1e8-7977-4b67-b65c-f009b5e88a3d",
    "SAOTS": "b3f17ecf-13f1-44c3-bc56-8f7f907c5699",
    "E2EEU": "bdd01534-d00a-485b-9195-36941eb6a8f6"
}

canadaids = {
    "OmniNA": "3bf4ce61-bb0b-4234-8d6b-28610ab5f49e",
    "PO3NA": "220eb259-f649-428f-a582-4443318e114c",
    "E2ENA": "5955f262-c93c-4065-b15f-08e38274cefd",
}

germanyids = {
    "FTBI": "abc80744-8c05-45d7-a887-e6025d736214",
    "ATM3R": "99efee7b-bbeb-41f0-b58e-b78313098b80",
    "GTNH": "36d09f34-b8f9-490f-a2dc-49c8471e119f",
    "DDSSEU": "92a2c592-1c54-4e6e-aa89-8a2c777d5f6b"
}

ids = {
    "OmniEU": "c109582e-dc78-4a24-b256-630afca1b88c",
    "PO3Titan": "6d8aa79c-a242-488a-b099-f018ec3749a4",
    "MCE": "3fa2f1e8-7977-4b67-b65c-f009b5e88a3d",
    "SAOTS": "b3f17ecf-13f1-44c3-bc56-8f7f907c5699",
    "E2EEU": "bdd01534-d00a-485b-9195-36941eb6a8f6",
    "OmniNA": "3bf4ce61-bb0b-4234-8d6b-28610ab5f49e",
    "PO3NA": "220eb259-f649-428f-a582-4443318e114c",
    "E2ENA": "5955f262-c93c-4065-b15f-08e38274cefd",
    "FTBI": "abc80744-8c05-45d7-a887-e6025d736214",
    "ATM3R": "99efee7b-bbeb-41f0-b58e-b78313098b80",
    "GTNH": "36d09f34-b8f9-490f-a2dc-49c8471e119f",
    "DDSSEU": "92a2c592-1c54-4e6e-aa89-8a2c777d5f6b"
}

def download(url, filename, node):

    if node == "london":
        url = nodes["london"] + url
    elif node == "canada":
        url = nodes["canada"] + url
    elif node == "germany":
        url = nodes["germany"] + url



    r = requests.get(url, allow_redirects=True, auth=auths)

    dir_path = os.getcwd()

    open(dir_path + "/" + filename, 'wb').write(r.content)

node = sys.argv[1]
server = sys.argv[2]

if node == "london":
    serverid = londonids[server]
    toAdd = nodes["london"]
elif node == "canada":
    serverid = canadaids[server]
    toAdd = nodes["canada"]
elif node == "germany":
    serverid = germanyids[server]
    toAdd = nodes["germany"]

url = toAdd + serverid + "/crash-reports/"

r = requests.get(url, auth=auths)

if r.status_code != 404:
    soup = bs4.BeautifulSoup(r.content, features="lxml")
    a = soup.findAll('a')

    format = "%Y-%m-%d_%H.%M"
    datetime_obj = []
    todl = ""

    for x in range(len(a)):
        s = a[x].contents[0]
        # print(s)
        match = re.search('\d{4}-\d{2}-\d{2}_\d{2}.\d{2}', s)
        date = datetime.datetime.strptime(match.group(), format)
        if date != None:
            datetime_obj.append(date)
        maxdate = max(datetime_obj)
        if maxdate == date:
            todl = s

    if node == "london":
        serverid = londonids[server]
        # toAdd = nodes["london"]
    elif node == "canada":
        serverid = canadaids[server]
        # toAdd = nodes["canada"]
    elif node == "germany":
        serverid = germanyids[server]
        # toAdd = nodes["germany"]

    url = serverid + "/crash-reports/" + todl

    dir_path = os.getcwd()

    download(url, todl, node)
    # open(dir_path + "/whereisthefile.txt", 'w').write(todl)
# print(url)
