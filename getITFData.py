import requests
import pprint as pp
import json
import Player
import datetime

def getITFData(curDict):
    data_headers = {
        "Host": "www.itftennis.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer":"https://www.itftennis.com/en/rankings/mens-world-tennis-tour-rankings/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Cookie": "visid_incap_178373=BBf/6TjpSbW4kT7P31BruoXrHWAAAAAAQUIPAAAAAADwJLOVymNgHvTCYYNSJvcb; incap_ses_890_178373=LrhsbgobkCZqAHHIh+pZDGIDIGAAAAAAn8beg+LNNlnAx9qiN82eHw==; _ga=GA1.2.694004469.1612573575; _gid=GA1.2.1369537440.1612573575; _fbp=fb.1.1612573574637.361756464; ARRAffinity=9027cc01602a77f2d2d43ef4f924cd969300186ff9c3202425c3ed52b05be0c0; ARRAffinitySameSite=9027cc01602a77f2d2d43ef4f924cd969300186ff9c3202425c3ed52b05be0c0; __gads=ID=c987a86b43c78508-22d96f96b2b80053:T=1612573575:RT=1612573575:S=ALNI_MZgSlSuPzHEgo5bn4uh0-VtkZEVcQ",
        "TE": "Trailers"
    }
    site = requests.get("https://www.itftennis.com/Umbraco/Api/PlayerRankApi/GetPlayerRankings?circuitCode=MT&matchTypeCode=S&ageCategoryCode=&take=100&skip=100", headers = data_headers)
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

playerDict = {}
getITFData(playerDict)
for player in playerDict.values():
    print(player.name + ", Age: " + str(player.age) + ", Country: " + player.country + ", status: " + player.status + ", site: " + str(player.site) + ", info: " + str(player.info) + "\n")