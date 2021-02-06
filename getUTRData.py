import Player
import requests
import json
import pprint as pp
from bs4 import BeautifulSoup


def getUTRData(curDict): 
    site = requests.get("https://agw-prod.myutr.com/v2/player/top?gender=M&tags=U18")
    data = site.json()

    for player in data: 
        pName = player["displayName"].encode("utf-8")
        if pName not in curDict:
            curDict[pName] = Player.Player(pName, -1, player["nationality"].encode("utf-8"), "null", {"UTR" : player["utr"]}, {"Pro":"null"})
    return curDict

# playerDict = {}
# getUTRData(playerDict)
# for player in playerDict.values():
#     print(player.name + ", Age: " + str(player.age) + ", Country: " + player.country + ", status: " + player.status + ", site: " + str(player.site) + ", info: " + str(player.info) + "\n")