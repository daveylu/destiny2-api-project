from authorization import *
"""
File Description: This file contains functions for the collection of various data
through Post Game Carnage Reports.
All functions will return info in a dictionary on time played (in seconds),
opponents defeated, number of deaths, efficiency (the Destiny name for KDA),
and whether or not you completed the activity or failed the activity.
"""
# #hardcoded player ID info: will remove when not testing

# playerName = "daveylu"
# membershipID = 4611686018483306200
# membershipType = 3
# characterID = 2305843009404396625

#returns standard info about the past 30 raids
def raidActivityHistory(membershipID, membershipType, characterID):
    r = requests.get(rootPath + f"/Destiny2/{membershipType}/Account/{membershipID}/Character/{characterID}/Stats/Activities/?count=30&mode=4&page=0", headers = headers)
    raidHistory = r.json()
    result = []
    for i in range(len(raidHistory["Response"]["activities"])):
        timePlayed = raidHistory["Response"]["activities"][i]["values"]["timePlayedSeconds"]["basic"]["value"]
        opponentsDefeated = raidHistory["Response"]["activities"][i]["values"]["opponentsDefeated"]["basic"]["value"]
        deaths = raidHistory["Response"]["activities"][i]["values"]["deaths"]["basic"]["value"]
        efficiency = raidHistory["Response"]["activities"][i]["values"]["efficiency"]["basic"]["value"]
        completionReason = raidHistory["Response"]["activities"][i]["values"]["completionReason"]["basic"]["value"]
        result.append({"timePlayed": timePlayed, "opponentsDefeated": opponentsDefeated, "deaths": deaths, "efficiency": efficiency, "completionReason": completionReason})
    return result

#returns standard info about the past 30 strikes
def strikeActivityHistory(membershipID, membershipType, characterID):
    r = requests.get(rootPath + f"/Destiny2/{membershipType}/Account/{membershipID}/Character/{characterID}/Stats/Activities/?count=30&mode=3&page=0", headers = headers)
    strikeHistory = r.json()
    result = []
    for i in range(len(strikeHistory["Response"]["activities"])):
        timePlayed = strikeHistory["Response"]["activities"][i]["values"]["timePlayedSeconds"]["basic"]["value"]
        opponentsDefeated = strikeHistory["Response"]["activities"][i]["values"]["opponentsDefeated"]["basic"]["value"]
        deaths = strikeHistory["Response"]["activities"][i]["values"]["deaths"]["basic"]["value"]
        efficiency = strikeHistory["Response"]["activities"][i]["values"]["efficiency"]["basic"]["value"]
        completionReason = strikeHistory["Response"]["activities"][i]["values"]["completionReason"]["basic"]["value"]
        result.append({"timePlayed": timePlayed, "opponentsDefeated": opponentsDefeated, "deaths": deaths, "efficiency": efficiency, "completionReason": completionReason})
    return result

#returns standard info about the past 30 nightfalls and legendary lost sectors
#as well as number of points you scored in NFs and LLSs, and team score for NFs
#Limitation: can only get 30 total for number of NFs and LLSs combined, due to API limitiations
def nightfallLLSActivityHistory(membershipID, membershipType, characterID):
    r = requests.get(rootPath + f"/Destiny2/{membershipType}/Account/{membershipID}/Character/{characterID}/Stats/Activities/?count=30&mode=46&page=0", headers = headers)
    nightfallHistory = r.json()
    nightfalls = []
    legendaryLostSectors = []
    for i in range(len(nightfallHistory["Response"]["activities"])):
        referenceID = nightfallHistory["Response"]["activities"][i]["activityDetails"]["referenceId"]
        r = requests.get(rootPath + f"/Destiny2/Manifest/DestinyActivityDefinition/{referenceID}/", headers = headers)
        activityInfo = r.json()
        activityName = activityInfo["Response"]["displayProperties"]["name"]
        timePlayed = nightfallHistory["Response"]["activities"][i]["values"]["timePlayedSeconds"]["basic"]["value"]
        opponentsDefeated = nightfallHistory["Response"]["activities"][i]["values"]["opponentsDefeated"]["basic"]["value"]
        deaths = nightfallHistory["Response"]["activities"][i]["values"]["deaths"]["basic"]["value"]
        efficiency = nightfallHistory["Response"]["activities"][i]["values"]["efficiency"]["basic"]["value"]
        completionReason = nightfallHistory["Response"]["activities"][i]["values"]["completionReason"]["basic"]["value"]
        yourScore = nightfallHistory["Response"]["activities"][i]["values"]["score"]["basic"]["value"]
        teamScore = nightfallHistory["Response"]["activities"][i]["values"]["teamScore"]["basic"]["value"]
        if("ordeal" in activityName.lower()):
            nightfalls.append({"timePlayed": timePlayed, "opponentsDefeated": opponentsDefeated, "deaths": deaths, "efficiency": efficiency, "completionReason": completionReason, "yourScore": yourScore, "teamScore": teamScore})
        else:
            legendaryLostSectors.append({"timePlayed": timePlayed, "opponentsDefeated": opponentsDefeated, "deaths": deaths, "efficiency": efficiency, "completionReason": completionReason, "yourScore": yourScore, "teamScore": teamScore})
    
    return nightfalls, legendaryLostSectors


#returns standard info for the previous 30 Gambit matches, as well as how many motes banked by you.
def gambitActivityHistory(membershipID, membershipType, characterID):
    r = requests.get(rootPath + f"/Destiny2/{membershipType}/Account/{membershipID}/Character/{characterID}/Stats/Activities/?count=30&mode=63&page=0", headers = headers)
    gambitHistory = r.json()
    result = []
    for i in range(len(gambitHistory["Response"]["activities"])):
        timePlayed = gambitHistory["Response"]["activities"][i]["values"]["timePlayedSeconds"]["basic"]["value"]
        opponentsDefeated = gambitHistory["Response"]["activities"][i]["values"]["opponentsDefeated"]["basic"]["value"]
        deaths = gambitHistory["Response"]["activities"][i]["values"]["deaths"]["basic"]["value"]
        efficiency = gambitHistory["Response"]["activities"][i]["values"]["efficiency"]["basic"]["value"]
        motesBanked = gambitHistory["Response"]["activities"][i]["values"]["score"]["basic"]["value"]

        #standing = 0 means victory, standing = 1 means defeat
        standing = gambitHistory["Response"]["activities"][i]["values"]["standing"]["basic"]["value"]
        result.append({"timePlayed": timePlayed, "opponentsDefeated": opponentsDefeated, "deaths": deaths, "efficiency": efficiency, "motesBanked": motesBanked, "standing": standing})
    return result

#returns standard info for dungeons in the game
#due to API limitations (aka Bungie spaghetti code), Shattered Throne is not included (due to being classified as as story mission)
def dungeonActivityHistory(membershipID, membershipType, characterID):
    r = requests.get(rootPath + f"/Destiny2/{membershipType}/Account/{membershipID}/Character/{characterID}/Stats/Activities/?count=30&mode=63&page=0", headers = headers)
    dungeonHistory = r.json()
    result = []
    for i in range(len(dungeonHistory["Response"]["activities"])):
        timePlayed = dungeonHistory["Response"]["activities"][i]["values"]["timePlayedSeconds"]["basic"]["value"]
        opponentsDefeated = dungeonHistory["Response"]["activities"][i]["values"]["opponentsDefeated"]["basic"]["value"]
        deaths = dungeonHistory["Response"]["activities"][i]["values"]["deaths"]["basic"]["value"]
        efficiency = dungeonHistory["Response"]["activities"][i]["values"]["efficiency"]["basic"]["value"]
        completionReason = dungeonHistory["Response"]["activities"][i]["values"]["completionReason"]["basic"]["value"]
        result.append({"timePlayed": timePlayed, "opponentsDefeated": opponentsDefeated, "deaths": deaths, "efficiency": efficiency, "completionReason": completionReason})
    return result
