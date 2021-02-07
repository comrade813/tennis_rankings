from Player import Player
import requests
import json
import pprint as pp
from bs4 import BeautifulSoup
import binascii
import urllib
import json
from common_functions import *

def login():
    s = requests.Session()
    login_url = "https://app.myutr.com/api/v1/auth/login"
    login_headers = {
        "Content-Length": "58",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "app.myutr.com",
    }

    payload = {
        "email": "KThorne@gtaa.gatech.edu",
        "password": "Jackets18"
    }

    response = s.post(login_url, data=json.dumps(payload), headers=login_headers)
    return s

def getUTRData(masterDict):
    s = login()

    data_header = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://app.myutr.com",
        "Referer": "https://app.myutr.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-User": "?1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
    }

    tags = ["U14", "U16", "U18", "HighSchool"]
    url = "https://agw-prod.myutr.com/v2/player/top?gender=M&tags="
    for t in tags:
        data_url = url+t
        data = s.get(data_url, headers=data_header, cookies=s.cookies)
        if data.status_code != 200:
            print("Something went wrong")
            return False
        players = json.loads(data.content)
        for player in players:
            if float(player["utr"]) > 11:
                name = player["displayName"]
                if name in masterDict.keys():
                    if "UTR" not in masterDict[name].site:
                        print("\tUpdating " + name + ", UTR: " + str(player["utr"]))
                        masterDict[name].site["UTR"] = player["utr"]
                    else:
                        print(name + "is up to date")
                else:
                    print("\tAdding " + name + ", UTR: " + str(player["utr"]))
                    profile = s.get("https://agw-prod.myutr.com/v1/player/"+str(player["id"])+"/profile")
                    age = json.loads(profile.content)["age"] if json.loads(profile.content)["age"] != None else ("< "+t)
                    if not isinstance(age, str) and age > 19:
                        continue
                    masterDict[name] = Player(name, age, player["nationality"],"not professional",
                                              {"UTR": player["utr"]}, {})
            else:
                break
    return True