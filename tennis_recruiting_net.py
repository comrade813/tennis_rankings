import requests
from bs4 import BeautifulSoup
from datetime import date
import hashlib
import hmac
import binascii
import urllib
import json
import Player

def hash_password(session_id):
    password = "kenny"

    password = hmac.new(password.encode(), password.encode(), digestmod=hashlib.sha256).hexdigest()
    #print(password.encode())
    password = hmac.new(session_id.encode(), password.encode(), digestmod=hashlib.sha256).hexdigest()
    #print(password)

    return password

def check_cookies(c1, c2):
    if c1 == c2:
        print("Cookies working")
    else:
        print("Cookies changed!!!")

def retrieve_tennis_recruiting_net(masterDict):
    headers = {
        "Host": "www.tennisrecruiting.net",
        "Connection": "close",
        "Content-Length": "119",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.tennisrecruiting.net",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.tennisrecruiting.net/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }
    s = requests.Session()
    s.get("https://www.tennisrecruiting.net")
    username = "kthorne"
    payload = {
        "login_username": username,
        "login_hash": "a",
        "login_submit": "Sign In"
    }
    login_url = "https://www.tennisrecruiting.net/ajax/login.asp"
    post = s.post(login_url, headers=headers, cookies=s.cookies, data=payload)
    payload["login_hash"] = hash_password(s.cookies.get_dict()["sessionid"])
    post = s.post(login_url, headers=headers, cookies=s.cookies, data=payload)
    standard = s.cookies
    if json.loads(post.content.decode())["activated"]:
        print("Login Success")
    else:
        print(post.content)
        print("Login Failed")
        return False
    
    data_headers = {
        "Host": "www.tennisrecruiting.net",
        "Connection": "close",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.tennisrecruiting.net/list.asp?id=1215&order=rank&extra=&page=2",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }
    data_url = "https://www.tennisrecruiting.net/list.asp?id=1215&order=rank&extra=&page=2"
    check_cookies(standard, s.cookies)
    page = s.get(data_url, headers=data_headers, cookies=s.cookies)
    #pretty_print_POST(page.request)
    #print(page.status_code)
    #print(page.content)
    check_cookies(standard, s.cookies)
    soup = BeautifulSoup(page.content, "html.parser")
    
    if len(str(soup.find_all("script")[9]).splitlines()) < 11:
        print("Bad Site")
        return False

    if str(soup.find_all("script")[9]).splitlines()[10].split(" =")[1].strip(" \'\";") == standard["sessionid"]:
        print("Session ID Good")
    else:
        print("Session ID Changed")
        return False
    if(str(soup.find_all("script")[9]).splitlines()[11].split(" =")[1].strip(" \'\";")) == "50610":
        print("Good User ID")
    else:
        print("Bad User ID")
        return False
    
    # print(soup.findAll("tr", id=True))
    urlTemp = "https://www.tennisrecruiting.net/list.asp?id={0}&order=rank&extra=&page={1}"
    levels = {"Juniors":"1225", "Sophomores":"1235", "Freshman":"1245", "8th Graders":"1255"}
    for grade in levels.keys():
        for x in range(1,2):
            print("Checking " + grade)
            getTRNData(masterDict, urlTemp.format(levels[grade], x), s) 
    # for player in curDict:
    #     curP = curDict[player]
    #     print(curP.name + ", Age: " + str(curP.age) + ", Country: " + curP.country + ", Status: " + str(curP.status) + ", Site: " + str(curP.site) + ", Info: " + str(curP.info))
    

def getTRNData(curDict, page, s):
    data_headers = {
        "Host": "www.tennisrecruiting.net",
        "Connection": "close",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }
    site = s.get(page, headers = data_headers, cookies=s.cookies)
    soup = BeautifulSoup(site.content, "html.parser")
    playerList = soup.findAll("tr", id=True)
    template = "https://www.tennisrecruiting.net/player.asp?id="
    for player in playerList:
        playerURL = template + player["id"]
        pSite = s.get(playerURL, cookies=s.cookies)
        pSoup = BeautifulSoup(pSite.content, "html.parser")
        data = str(pSoup.find_all("script")[21])
        data = json.loads(data[data.find("{"):data.rfind("}")+1])
        name = data["header"]["fullname"]
        if data["weekly_rankings"].get("utr") != None and data["weekly_rankings"]["utr"]["rating"] < 11:
            continue
        if name not in curDict:
            print("\tAdding " + name)
            curDict[name] = Player.Player(name, -1, "USA", data["header"]["grade"],
                            {"TRN": data["header"]["stars"] if data["header"]["stars"] < 6 else "Blue Chip"}, {})
            if data["weekly_rankings"].get("utr") != None:
                curDict[name].site["UTR"] = data["weekly_rankings"]["utr"]["rating"]
        else:
            print("\tUpdating " + name)
            curDict[name].status = data["header"]["grade"]
            curDict[name].country = "USA"
            curDict[name].site["TRN"] = data["header"]["stars"] if data["header"]["stars"] < 6 else "Blue Chip"
            if "UTF" not in curDict[name].site.keys() and data["weekly_rankings"].get("utr") != None:
                curDict[name].site["Tennis Recruiting Rank"] = data["weekly_rankings"]["utr"]["rating"]