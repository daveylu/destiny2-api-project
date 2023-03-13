"""
File Description: This file contains functions that will get the account/character's
various information regarding weapons, and weapon usage
ex. most used Exotic weapon per character, most used weapon type overall, etc.
"""

from authorization import *


def getMostUsedWeaponClassAccount(membershipID, membershipType): #returns the most used weapon class for the account

    weaponUsage = requests.get(rootPath + f"/Destiny2/{membershipType}/Account/{membershipID}/Stats/?groups=2", headers = headers)
    weaponUsage = weaponUsage.json()

    mostKills = -1
    bestWeapon = "who knows"

    for weapons in weaponUsage["Response"]["mergedAllCharacters"]["results"]["allPvE"]["allTime"]:
        if("Precision" not in weapons and weapons != "activitesEntered"):
            weaponType = weaponUsage["Response"]["mergedAllCharacters"]["results"]["allPvE"]["allTime"][weapons]["statId"]
            weaponKills = weaponUsage["Response"]["mergedAllCharacters"]["results"]["allPvE"]["allTime"][weapons]["basic"]["value"]
            if(weaponKills > mostKills):
                mostKills = weaponKills
                bestWeapon = weaponType
    return bestWeapon[11:], mostKills


#returns the most used exotic weapon's hash value, name, and its kills for the character
def getMostUsedExoticWeaponCharacter(membershipID, membershipType, characterID):

    response = requests.get(rootPath + f"/Destiny2/{membershipType}/Account/{membershipID}/Character/{characterID}/Stats/UniqueWeapons/", headers = headers)
    response = response.json()

    mostKills = -1
    bestExoticID = -1
    for d in response["Response"]["weapons"]:
        referenceID = d["referenceId"]
        kills = d["values"]["uniqueWeaponKills"]["basic"]["value"]
        if(kills > mostKills):
            mostKills = kills
            bestExoticID = referenceID


    response = requests.get(rootPath + f"/Destiny2/Manifest/DestinyInventoryItemDefinition/{bestExoticID}/", headers = headers)
    response = response.json()

    exoticWeaponName = response["Response"]["displayProperties"]["name"]
    return bestExoticID, exoticWeaponName, mostKills

#returns a dictionary for kinetic/energy/heavy, each containing the hash value, name, and URL for the icon
def getEquippedWeaponsCharacter(membershipID, membershipType, characterID): 
    equippedWeapons = {"kinetic": dict(), "energy": dict(), "power": dict()}
    response = requests.get(rootPath + f"/Destiny2/{membershipType}/Profile/{membershipID}/Character/{characterID}/?components=205", headers = headers)
    response = response.json()
    for i in range(3):
        if(i == 0):
            weaponSlot = "kinetic"
        elif(i == 1):
            weaponSlot = "energy"
        else:
            weaponSlot = "power"
        weaponHash = response["Response"]["equipment"]["data"]["items"][i]["itemHash"]
        weaponInfo = requests.get(rootPath + f"/Destiny2/Manifest/DestinyInventoryItemDefinition/{weaponHash}/", headers = headers)
        weaponInfo = weaponInfo.json()
        weaponName = weaponInfo["Response"]["displayProperties"]["name"]
        weaponIconURL = weaponInfo["Response"]["displayProperties"]["icon"]
        weaponType = weaponInfo["Response"]["itemTypeDisplayName"]
        equippedWeapons[weaponSlot]["weaponName"] = weaponName
        equippedWeapons[weaponSlot]["weaponIconURL"] = weaponIconURL
        equippedWeapons[weaponSlot]["weaponType"] = weaponType
    return equippedWeapons

