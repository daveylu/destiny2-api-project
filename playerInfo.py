import time
import calendar
from authorization import *
from playerWeaponInfo import *

"""
File description: This file contains functions that will get the information of the person
that is logged in.

Time stuff taken from the time documentation here: https://docs.python.org/3/library/calendar.html#calendar.timegm
As well as here: https://wiki.python.org/moin/WorkingWithTime
"""
# #hardcoded player ID info: will remove when not testing

playerName = "daveylu"
membershipID = 4611686018483306200
membershipType = 3
characterID = 2305843009404396625

#returns the game membershipID (used for Destiny2 API calls) and the platform of the current user
def getPlayerDestinyInfo(): 
    playerInfo = requests.get(rootPath + "/User/GetMembershipsForCurrentUser/", headers = headers)
    playerInfo = playerInfo.json()
    membershipID = playerInfo["Response"]["destinyMemberships"][0]["membershipId"]
    membershipType = playerInfo["Response"]["destinyMemberships"][0]["membershipType"]
    playerName = playerInfo["Response"]["destinyMemberships"][0]["LastSeenDisplayName"]
    return playerName, membershipID, membershipType

#gets info about characters for the given accountID and platform
def getPlayerCharacterInfo(membershipID, membershipType): 

    characterInfo = dict()

    response = requests.get(rootPath + f"/Destiny2/{membershipType}/Profile/{membershipID}/?components=200", headers = headers)
    response = response.json()

    for characterID in response["Response"]["characters"]["data"]:

        emblemPath = response["Response"]["characters"]["data"][characterID]["emblemPath"]
        classType = response["Response"]["characters"]["data"][characterID]["classType"]

        if(classType == 0):
            characterClass = "Titan"
        elif(classType == 1):
            characterClass = "Hunter"
        else:
            characterClass = "Warlock"

        characterInfo[characterID] = dict()

        characterInfo[characterID]["characterClass"] = characterClass
        characterInfo[characterID]["emblemPath"] = emblemPath

    return characterInfo

#returns the ID number for the clan that the player is in
def getPlayerClan(membershipID, membershipType):
    r = requests.get(rootPath + f"/GroupV2/User/{membershipType}/{membershipID}/0/1/", headers = headers)
    clanInfo = r.json()
    clanID = clanInfo["Response"]["results"][0]["group"]["groupId"]
    return clanID

#returns a list containing the membershipIDs and membershipTypes of all players (including the user) in the user's fireteam
def getAllPlayerFireteamMembershipIDs(membershipID, membershipType):
    fireteamMembershipInfo = []

    r = requests.get(rootPath + f"/Destiny2/{membershipType}/Profile/{membershipID}/?components=1000", headers = headers)
    value = r.json()

    for i in range(len(value["Response"]["profileTransitoryData"]["data"]["partyMembers"])):
        memberInfo = value["Response"]["profileTransitoryData"]["data"]["partyMembers"][i]
        membershipID = memberInfo["membershipId"]
        displayName = memberInfo["displayName"]
        r = requests.get(rootPath + f"/Destiny2/SearchDestinyPlayer/-1/{displayName}/", headers = headers)
        r = r.json()
        possibleMembers = r["Response"]
        for i in range(len(possibleMembers)):
            possibleMembershipID = possibleMembers[i]["membershipId"]
            if(membershipID == possibleMembershipID):
                membershipType = possibleMembers[i]["membershipType"]
        fireteamMembershipInfo.append( (membershipID, membershipType) )

    return fireteamMembershipInfo

#returns the characterID of the given membershipID that is currently online
def getCurrentlyOnlineCharacterIDfromMembershipID(membershipID, membershipType):
    r = requests.get(rootPath + f"/Destiny2/{membershipType}/Profile/{membershipID}/?components=204", headers = headers)
    r = r.json()
    bestTime = -1
    bestCharID = None
    for characterID in r["Response"]["characterActivities"]["data"]:
        currTime = r["Response"]["characterActivities"]["data"][characterID]["dateActivityStarted"]
        currTime = currTime[:-1]
        currTime = calendar.timegm(time.strptime(currTime, "%Y-%m-%dT%H:%M:%S"))
        if(currTime > bestTime):
            bestTime = currTime
            bestCharID = characterID
    return bestCharID

#returns a dictionary containing the whole fireteam, inputs are your membershipID and type
# key = membershipID, values = current characterID and equipped weapons, username, emblem path
def getPlayerFireteamInfo(membershipID, membershipType):
    fireteamMemberInfo = getAllPlayerFireteamMembershipIDs(membershipID, membershipType)
    fireteam = dict()

    for fireteamMemberID, fireteamMembershipType in fireteamMemberInfo:
        fireteam[fireteamMemberID] = dict()

        characterID = getCurrentlyOnlineCharacterIDfromMembershipID(fireteamMemberID, fireteamMembershipType)
        fireteam[fireteamMemberID]["characterID"] = characterID

        equippedWeapons = getEquippedWeaponsCharacter(fireteamMemberID, fireteamMembershipType, characterID)
        fireteam[fireteamMemberID]["equippedWeapons"] = equippedWeapons

        response = requests.get(rootPath + f"/Destiny2/{fireteamMembershipType}/Profile/{fireteamMemberID}/?components=100", headers = headers)
        accountInfo = response.json()
        playerName = accountInfo["Response"]["profile"]["data"]["userInfo"]["displayName"]
        fireteam[fireteamMemberID]["playerName"] = playerName

        response = requests.get(rootPath + f"/Destiny2/{fireteamMembershipType}/Profile/{fireteamMemberID}/Character/{characterID}/?components=200", headers = headers)
        characterInfo = response.json()
        emblemPath = characterInfo["Response"]["character"]["data"]["emblemPath"]
        fireteam[fireteamMemberID]["emblemPath"] = emblemPath

    return fireteam

#returns a dictionary mapping all incomplete milestones to their description
#except for the Master Class milestone, due to it being a temporary milestone.
def getPlayerMilestones(membershipID, membershipType, characterID):
    r = requests.get(rootPath + f"/Destiny2/{membershipType}/Profile/{membershipID}/Character/{characterID}/?components=202", headers = headers)

    characterProgression = r.json()
    milestones = dict()

    for milestoneHash in characterProgression["Response"]["progressions"]["data"]["milestones"]:
        r = requests.get(rootPath + f"/Destiny2/Manifest/DestinyMilestoneDefinition/{milestoneHash}/", headers = headers)
        milestoneInfo = r.json()
        name = milestoneInfo["Response"]["displayProperties"]["name"]
        if(name == "Master Class"):
            continue
        description = milestoneInfo["Response"]["displayProperties"]["description"]
        milestones[name] = description

    return milestones