import requests
import pprint as pp
import json
import Player
import datetime

def getITFData(curDict):
    site = requests.get("https://www.itftennis.com/Umbraco/Api/PlayerRankApi/GetPlayerRankings?circuitCode=JT&playerTypeCode=B&ageCategoryCode=&juniorRankingType=itf&take=500&skip=0")
    rawData = site.json()
    playerData = rawData["items"]
    for player in playerData:
        pName = player["playerGivenName"].encode("utf-8") + " " + player["playerFamilyName"].encode("utf-8")
        age = datetime.date.today().year - player["birthYear"]
        if pName not in curDict:
            curDict[pName] = Player.Player(pName, datetime.date.today().year - player["birthYear"], player["playerNationalityCode"].encode("utf-8"), "not professional", {"ITF": player["points"]}, {})
        else:
            if curDict[pName].age == -1: 
                curDict[pName].age = age
            curDict[pName].site['ITF'] = player["points"]

# playerDict = {}
# getITFData(playerDict)
# for player in playerDict.values():
#     print(player.name + ", Age: " + str(player.age) + ", Country: " + player.country + ", status: " + player.status + ", site: " + str(player.site) + ", info: " + str(player.info) + "\n")