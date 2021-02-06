import Player
import requests
import json
import pprint as pp
from bs4 import BeautifulSoup


playerDict = {}
def getUTRData(curDict): 
    site = requests.get("https://agw-prod.myutr.com/v2/player/top?gender=M&tags=U18")
    data = site.json()

    for player in data: 
        pName = player["displayName"].encode("utf-8")
        if pName not in curDict:
            playerPage = requests.get("https://app.myutr.com/profiles/"+str(player["id"])+ "?t=6")
            agesoup = BeautifulSoup(playerPage.content, "html.parser")
            sectionA = agesoup.find("span", class_= "aboutContent__bold__103cf")
            # sectionC = sectionB.find("div", id = "myutr-app-wrapper")
            # sectionD = sectionC.find("div", id = "myutr-app-body")
            # sectionE = sectionD.find
            if (pName == "Luca Nardi"):
                print(sectionA)
                print(playerPage.content)
            # sectionA = agesoup.find(id = "myutr-app-body")
            # sectionB = sectionA.find(class_ = "profilePage__playerProfile__au7PU")
            # print(sectionB.prettify())
            
            curDict[pName] = Player.Player(pName, -1, player["nationality"].encode("utf-8"), "null", {"UTR" : player["utr"]}, {"Pro":"null"})
    return curDict


getUTRData(playerDict)
# for player in playerDict.values():
#     print(player.name + ", Age: " + str(player.age) + ", Country: " + player.country + ", status: " + player.status + ", site: " + str(player.site) + ", info: " + str(player.info) + "\n")