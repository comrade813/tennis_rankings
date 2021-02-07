import getUTRData as UTR
import getITFData as ITF
import pprint as pp

masterDict = {}
def tempMain(playerDict):
    UTR.getUTRData(playerDict)
    ITF.getITFData(playerDict)
    return playerDict

tempMain(masterDict)

# for player in masterDict.values():
#     print(player.name + ", Age: " + str(player.age) + ", Country: " + player.country + ", status: " + player.status + ", site: " + str(player.site) + ", info: " + str(player.info) + "\n")

# print(len(masterDict))