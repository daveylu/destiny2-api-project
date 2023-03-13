"""
This file will contain functions for figuring out what roles people have,
as well as have the info on the recommended activity if so.

Some data on shields and champions in each activity taken from: https://docs.google.com/spreadsheets/d/1tB87AL467rpjsIAe6PkMdVI3hHQ9rGFbcwQCDCACRZI/edit#gid=403041532

Nightfalls, Legendary Lost Sectors, Dungeons, and Empire Hunts only have weapon recommendations,
due to the nature of the activity. Their functions will just return a list of the recommended weapons
and shields for specific activities. (Dungeons do not have shield info due to no Match Game modifier)

Raids and Gambit will take in the player's weapons, and return the roles that the player can fulfill.
These roles for raids were created through my experience and general community consensus.
Weapon recommendations for NFs, LLSs, and EHs will be obsolete in Season 14 due to Champion mods changing.
"""

#Nightfalls
def devilsLair():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher"],
        "elements": ["Arc", "Void", "Solar"]
    }
    return values

def armsDealer():
    values = {
        "primary": ["Hand Cannon", "Pulse Rifle", "Scout Rifle"],
        "special": ["Eriana's Vow", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "Sword"],
        "elements": ["Void", "Solar", "Arc"]
    }
    return values

def provingGrounds():
    values = {
        "primary": ["Skyburner's Oath", "Hand Cannon", "Pulse Rifle", "Scout Rifle"],
        "special": ["Sniper Rifle", "Eriana's Vow"],
        "power": ["Rocket Launcher", "Grenade Launcher", "Sword"],
        "elements" : ["Void", "Solar", "Arc"]
    }
    return values

def wardenOfNothing():
    values = {
        "primary": ["Hand Cannon", "Pulse Rifle", "Scout Rifle", "Combat Bow", "Submachine Gun"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "Sword"],
        "elements": ["Void", "Solar"]
    }
    return values

def fallenSaber():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher"],
        "elements" : ["Arc", "Void"]
    }
    return values

def insightTerminus():
    values = {
        "primary": ["Hand Cannon", "Pulse Rifle", "Scout Rifle"],
        "special": ["Eriana's Vow", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "Sword"],
        "elements": ["Void", "Arc"]
    }
    return values


#Legendary Lost Sectors

def exodusGarden2A():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "The Lament"],
        "elements" : ["Void"]
    }
    return values

def velesLabyrinth():
    values = {
        "primary": ["Hand Cannon", "Pulse Rifle", "Scout Rifle"],
        "special": ["Eriana's Vow", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "Sword", "The Lament"],
        "elements": ["Void", "Solar"]
    }
    return values

def perdition():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "The Lament"],
        "elements" : ["Arc", "Void"]
    }
    return values

def bunkerE15():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "The Lament"],
        "elements" : ["Void"]
    }
    return values

def concealedVoid():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "The Lament"],
        "elements" : ["Arc", "Solar", "Void"]
    }
    return values

def k1Communion():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "The Lament"],
        "elements" : ["Solar", "Void"]
    }
    return values

def k1Logistics():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "The Lament"],
        "elements" : ["Arc", "Solar"]
    }
    return values

def k1CrewQuarters():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "The Lament"],
        "elements" : ["Solar"]
    }
    return values

def k1Revelations():
    values = {
        "primary": ["Hand Cannon", "Pulse Rifle", "Scout Rifle"],
        "special": ["Eriana's Vow", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher", "Sword", "The Lament"],
        "elements": ["Arc"]
    }
    return values


#Empire Hunts

def technocrat():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher"],
        "elements" : ["Arc"]
    }
    return values

def warrior():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher"],
        "elements" : ["Arc", "Solar"]
    }
    return values

def darkPriestess():
    values = {
        "primary": ["Combat Bow", "Submachine Gun", "Scout Rifle"],
        "special": ["Eriana's Vow", "Divinity", "Sniper Rifle"],
        "power": ["Rocket Launcher", "Grenade Launcher"],
        "elements" : ["Void", "Arc"]
    }
    return values


#Dungeons:

def shatteredThrone():
    values = {
        "primary": ["Pulse Rifle", "Auto Rifle", "Hand Cannon"],
        "special": ["Sniper Rifle", "Shotgun", "Grenade Launcher"],
        "power": ["Xenophage", "Whisper of the Worm", "Anarchy", "Sword"]
    }
    return values

def pitOfHeresy():
    values = {
        "primary": ["Submachine Gun", "Auto Rifle", "Sidearm"],
        "special": ["Shotgun", "Grenade Launcher"],
        "power": ["Xenophage", "Whisper of the Worm", "Anarchy", "Sword"]
    }
    return values

def prophecy():
    values = {
        "primary": ["Pulse Rifle", "Auto Rifle", "Submachine Gun"],
        "special": ["Shotgun", "Grenade Launcher"],
        "power": ["Xenophage", "Whisper of the Worm", "Anarchy", "Sword"]
    }
    return values


#Raids

def deepStoneCrypt_CryptSecurity(weapons):
    result = []
    operatorScore = 0
    elseScore = 0
    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        if(weaponSlot == "power"):
            operatorScore += 5
        elif(weaponType not in ["Scout Rifle", "Combat Bow", "Sniper Rifle"]):
            operatorScore += 5
            elseScore += 5
        else:
            weaponName = weapons[weaponSlot]["weaponName"]
            if(weaponName in ["Xenophage", "One Thousand Voices"] or
               weaponType in ["Rocket Launcher", "Grenade Launcher"]):
                operatorScore += 5
                elseScore += 5
    if(operatorScore >= 10):
        result.append("Operator")
    if(elseScore >= 10):
        result.append("Else")
    return result

def deepStoneCrypt_Atraks1(weapons):
    powerWeaponName = weapons["power"]["weaponName"]
    if(powerWeaponName == "The Lament"):
        return ["DPS"]
    else:
        return []

def deepStoneCrypt_Descent(weapons):
    return ["Any Role"]

def deepStoneCrypt_Taniks(weapons):
    result = []
    operatorScore = 0
    DPSScore = 0

    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponName == "Anarchy"):
            DPSScore += 5
        elif(weaponName == "Divinity"):
            operatorScore += 5
        if(weaponType == "Shotgun"):
            DPSScore += 5
        elif(weaponType in ["Rocket Launcher", "Grenade Launcher", "Sniper Rifle"]):
            DPSScore += 3
        elif(weaponType in ["Submachine Gun", "Auto Rifle"]):
            operatorScore += 5
        elif(weaponType in ["Hand Cannon", "Pulse Rifle", "Sidearm"]):
            operatorScore += 3
        elif(weaponType in ["Combat Bow", "Scout Rifle"]):
            operatorScore += 1

    if(operatorScore >= 10):
        result.append("Operator")
    if(DPSScore >= 10):
        result.append("DPS")
    return result

def lastWish_Kalli(weapons):
    result = []
    DPSScore = 0

    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponName == "Anarchy"):
            result.append("Glitcher")
        if(weaponType in ["Shotgun", "Sword"]):
            DPSScore += 5
        elif(weaponType in ["Fusion Rifle", "Grenade Launcher", "Rocket Launcher", "Sniper Rifle"]):
            DPSScore += 3
        else:
            DPSScore += 2

    if(DPSScore >= 10):
        result.append("DPS")
    return result

def lastWish_ShuroChi(weapons):
    result = []
    DPSScore = 0
    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponType in ["Submachine Gun", "Auto Rifle", "Sidearm", "Shotgun", "Grenade Launcher", "Sword"]):
            DPSScore += 5
        elif(weaponType in ["Pulse Rifle", "Hand Cannon", "Fusion Rifle", "Sniper Rifle"]):
            DPSScore += 3
        else:
            DPSScore += 2
    if(DPSScore >= 10):
        result.append("DPS")
    return result

def lastWish_Morgeth(weapons):
    result = []
    DPSScore = 0
    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponType in ["Pulse Rifle", "Hand Cannon", "Sniper Rifle", "Sword"]):
            DPSScore += 5
        elif(weaponType in ["Auto Rifle", "Fusion Rifle", "Grenade Launcher", "Shotgun"]):
            DPSScore += 4
        else:
            DPSScore += 1
    if(DPSScore >= 10):
        result.append("DPS")
    return result

def lastWish_Vault(weapons):
    result = []
    defenseScore = 0
    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponType in ["Submachine Gun", "Auto Rifle", "Sidearm", "Shotgun", "Grenade Launcher", "Sword"]):
            defenseScore += 5
        elif(weaponType in ["Fusion Rifle", "Machine Gun"]):
            defenseScore += 4
        elif(weaponType in ["Pulse Rifle", "Hand Cannon", "Sniper Rifle"]):
            defenseScore += 3
        else:
            defenseScore += 1
    if(defenseScore >= 10):
        result.append("Defense")
    return result

def lastWish_RivenCheese(weapons):
    powerWeaponType = weapons["power"]["weaponType"]
    powerWeaponName = weapons["power"]["weaponName"]
    if(powerWeaponType == "Sword"):
        return ["DPS"]
    elif(powerWeaponName == "Tractor Cannon"):
        return ["Debuff"]
    else:
        return []

def lastWish_RivenLegit(weapons):
    score = 0
    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponName in ["Xenophage", "One Thousand Voices"]):
            score += 5
        elif(weaponType in ["Pulse Rifle", "Hand Cannon", "Sniper Rifle"]):
            score += 5
        elif(weaponType in ["Rocket Launcher", "Grenade Launcher", "Auto Rifle"]):
            score += 4
        elif(weaponType in ["Combat Bow", "Fusion Rifle"]):
            score += 3
        elif(weaponType in ["Submachine Gun", "Sidearm", "Scout Rifle"]):
            score += 2
        else:
            score += 1
    if(score >= 10):
        return ["Prepared"]
    else:
        return ["Not Prepared"]

def lastWish_Queenswalk(weapons):
    score = 0
    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponType in ["Submachine Gun", "Auto Rifle", "Shotgun", "Grenade Launcher", "Machine Gun"]):
            score += 5
        elif(weaponType in ["Sidearm", "Pulse Rifle", "Hand Cannon", "Rocket Launcher"]):
            score += 4
        elif(weaponType in ["Fusion Rifle", "Sword"]):
            score += 3
        else:
            score += 2
    if(score >= 10):
        return ["Prepared"]
    else:
        return ["Not Prepared"]

def gardenOfSalvation_Evade(weapons):
    score = 0
    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponType in ["Auto Rifle", "PUlse Rifle", "Hand Cannon", "Combat Bow", "Submachine Gun", "Machine Gun"]):
            score += 5
        elif(weaponType in ["Rocket Launcher", "Grenade Launcher", "Fusion Rifle"]):
            score += 4
        elif(weaponType in ["Sword", "Sidearm"]):
            score += 3
        else:
            score += 1
    if(score >= 10):
        return ["Prepared"]
    else:
        return ["Not Prepared"]

def gardenOfSalvation_Summon(weapons):
    score = 0
    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponName == "The Lament"):
            score += 5
        elif(weaponType in ["Scout Rifle", "Pulse Rifle", "Hand Cannon", "Sniper Rifle", "Grenade Launcher", "Machine Gun"]):
            score += 5
        elif(weaponType in ["Auto Rifle", "Submachine Gun", "Rocket Launcher"]):
            score += 4
        else:
            score += 3
    if(score >= 10):
        return ["Prepared"]
    else:
        return ["Not Prepared"]
    
def gardenOfSalvation_ConsecratedMind(weapons):
    result = []
    eyesScore = 0
    motesScore = 0
    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponName == "Divinity"):
            result.append("Debuff")
        elif(weaponName in ["Whisper of the Worm", "Xenophage", "One Thousand Voices"]):
            result.append("DPS")
        elif(weaponType in ["Shotgun", "Auto Rifle"]):
            eyesScore += 5
            motesScore += 5
        elif(weaponType == "Submachine Gun"):
            eyesScore += 5
            motesScore += 4
        elif(weaponType in ["Pulse Rifle", "Hand Cannon"]):
            eyesScore += 3
            motesScore += 5
        elif(weaponType in ["Combat Bow", "Scout Rifle"]):
            motesScore += 1
        elif(weaponType in ["Grenade Launcher", "Fusion Rifle", "Rocket Launcher"]):
            eyesScore += 2
            motesScore += 3
        elif(weaponType == "Sniper Rifle"):
            eyesScore += 5
            motesScore += 2
        else:
            eyesScore += 1
            motesScore += 1

    if(eyesScore >= 7):
        result.append("Eyes")
    if(motesScore >= 7):
        result.append("Motes")
    return result

def gardenOfSalvation_SanctifiedMind(weapons):
    result = []
    buildScore = 0
    motesScore = 0
    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponName == "Divinity"):
            result.append("Debuff")
        elif(weaponName in ["Whisper of the Worm", "Xenophage", "One Thousand Voices"]):
            result.append("DPS")
        elif(weaponType in ["Pulse Rifle", "Hand Cannon", "Sniper Rifle"]):
            buildScore += 5
            motesScore += 3
        elif(weaponType == "Auto Rifle"):
            buildScore += 4
            motesScore += 5
        elif(weaponType in ["Sidearm", "Submachine Gun"]):
            buildScore += 3
            motesScore += 5
        elif(weaponType in ["Fusion Rifle", "Grenade Launcher"]):
            buildScore += 2
            motesScore += 5
        elif(weaponType in ["Combat Bow", "Scout Rifle"]):
            buildScore += 2
            motesScore += 1
        else:
            buildScore += 1
            motesScore += 1

    if(buildScore >= 7):
        result.append("Build")
    if(motesScore >= 7):
        result.append("Motes")
    return result

def gambit(weapons):
    result = []
    invaderScore = 0
    sentryScore = 0
    reaperScore = 0
    collectorScore = 0
    for weaponSlot in weapons:
        weaponType = weapons[weaponSlot]["weaponType"]
        weaponName = weapons[weaponSlot]["weaponName"]
        if(weaponName == "Malfeasance"):
            sentryScore += 8
        elif(weaponName in ["Xenophage", "One Thousand Voices"]):
            invaderScore += 5
            sentryScore += 5
            collectorScore += 5
        elif(weaponName in ["Eyes of Tomorrow", "Truth"]):
            invaderScore += 5
            sentryScore += 5
        elif(weaponType in ["Scout Rifle", "Combat Bow"]):
            invaderScore += 5
            sentryScore += 5
            collectorScore += 2
        elif(weaponType in ["Hand Cannon", "Pulse Rifle"]):
            invaderScore += 4
            sentryScore += 4
            reaperScore += 3
            collectorScore += 5
        elif(weaponType == "Auto Rifle"):
            invaderScore += 3
            sentryScore += 3
            reaperScore += 4
            collectorScore += 5
        elif(weaponType in ["Submachine Gun", "Sidearm"]):
            invaderScore += 1
            sentryScore += 1
            reaperScore += 5
            collectorScore += 4
        elif(weaponType == "Sniper Rifle"):
            invaderScore += 5
            sentryScore += 5
            reaperScore += 1
            collectorScore += 3
        elif(weaponType == "Shotgun"):
            invaderScore += 1
            sentryScore += 2
            reaperScore += 5
            collectorScore += 4
        elif(weaponType == "Fusion Rifle"):
            invaderScore += 2
            sentryScore += 3
            reaperScore += 4
            collectorScore += 5
        elif(weaponType == "Grenade Launcher"):
            invaderScore += 3
            sentryScore += 3
            reaperScore += 3
            collectorScore += 5
        elif(weaponType == "Sword"):
            sentryScore += 1
            reaperScore += 5
            collectorScore += 4
        elif(weaponType == "Rocket Launcher"):
            invaderScore += 4
            sentryScore += 5
            reaperScore += 2
            collectorScore += 4
        elif(weaponType == "Machine Gun"):
            invaderScore += 4
            sentryScore += 4
            reaperScore += 4
            collectorScore += 5
        else:
            invaderScore += 1
            sentryScore += 1
            reaperScore += 1
            collectorScore += 1
    if(invaderScore >= 10):
        result.append("Invader")
    if(sentryScore >= 10):
        result.append("Sentry")
    if(reaperScore >= 10):
        result.append("Reaper")
    if(collectorScore >= 10):
        result.append("Collector")
    return result

#weapons = {'kinetic': {'weaponName': 'The Messenger', 'weaponIconURL': '/common/destiny2_content/icons/5be3911505b3e65062c75537e725beed.jpg', 
#'weaponType': 'Pulse Rifle'}, 'energy': {'weaponName': "Salvager's Salvo", 'weaponIconURL': '/common/destiny2_content/icons/41fb6556236b906950a5c532452a010c.jpg', 'weaponType': 'Grenade Launcher'}, 'power': {'weaponName': 'The Lament', 'weaponIconURL': '/common/destiny2_content/icons/9976b41a3b121e9c191fa0b313eb6bf9.jpg', 'weaponType': 'Sword'}}

