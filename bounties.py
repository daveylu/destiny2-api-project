from authorization import *
from playerInfo import *

"""
This file contains functions related to bounties: the fetching of all available bounties
from common vendors, and catagorizing bounties into predefined catagories, for use after
recommending activities or weapons to the user.

Also, just to rant: IT IS SO GODDAMN HARD TO FIND STUFF IN THIS DAMN API, HOW TF WAS I SUPPOSED TO
KNOW THAT BOUNTIES ACTUALLY HAVE THEIR OWN IDENTIFYING HASH VALUE, I SPENT HOURS TRYING TO FIGURE OUT
HOW TO FILTER OUT THE OTHER CRAP BEFORE FINDING THIS RANDOM NUGGET OF KNOWLEDGE ON GITHUB
AHHHHHHHHHHHHHHHHHHHHHHHHHHH IM GONNA LOSE IT
"""

# #hardcoded player ID info: will remove when not testing
# playerName = "daveylu"
# membershipID = "4611686018483306200"
# membershipType = 3
# characterID = 2305843009404396625


#this fucntion gets all of the bounties from vendors listed below, available to the given character
#returns a dictionary mapping vendor names to their hash + their bounties
def allVendorBounties(membershipID, membershipType, characterID):

    #some constants for the vendors common to all players
    vendors = {
        "Variks": {"vendorHash": 2531198101},
        "Shaw Han": {"vendorHash": 1816541247},
        "Crow": {"vendorHash": 3611983588},
        "Hawthorne": {"vendorHash": 3347378076},
        "Lord Shaxx": {"vendorHash": 3603221665},
        "Devrim Kay": {"vendorHash": 396892126},
        "Banshee-44": {"vendorHash": 672118013},
        "Failsafe": {"vendorHash": 1576276905},
        "Commander Zavala": {"vendorHash": 69482069},
        "Drifter": {"vendorHash": 248695599},
        "Spider": {"vendorHash": 863940356},
        "Eris Morn": {"vendorHash": 1616085565},
        }

    #this section saves all of the bounties that the vendors are selling, to the vendors dict above
    for vendor in vendors:
        vendorHash = vendors[vendor]["vendorHash"]
        r = requests.get(rootPath + f"/Destiny2/{membershipType}/Profile/{membershipID}/Character/{characterID}/Vendors/{vendorHash}/?components=402", headers = headers)
        vendorItems = r.json()
        bounties = dict()
        for item in vendorItems["Response"]["sales"]["data"]:
            hashValue = vendorItems["Response"]["sales"]["data"][item]["itemHash"]
            r = requests.get(rootPath + f"/Destiny2/Manifest/DestinyInventoryItemDefinition/{hashValue}/", headers = headers)
            result = r.json()
            if(1784235469 in result["Response"]["itemCategoryHashes"]):
                name = result["Response"]["displayProperties"]["name"]
                description = result["Response"]["displayProperties"]["description"]
                bounties[name] = description
        vendors[vendor]["bounties"] = bounties
    return vendors

#catagorizes all currently available bounties into weapon type, location, activity
#returns a dictionary with catagories mapping to a list containing all relevant bounty names
#dictionary is split up into destinations and weapons
def catagorizeBounties(membershipID, membershipType, characterID):

    vendors = allVendorBounties(membershipID, membershipType, characterID)

    bountyCatagories = {
        "Destination/Activity": {          #dictionary with some catagories
            "Strikes": [],
            "Gambit": [],
            "EDZ": [],
            "Cosmodrome":[],
            "Europa":[],
            "Nessus":[],
            "Tangled Shore":[],
            "Moon": []
            },
        "Weapon": {
            "Submachine Gun": [],
            "Auto Rifle": [],
            "Sidearm": [],
            "Pulse Rifle": [],
            "Hand Cannon": [],
            "Bow": [], 
            "Scout Rifle": [],
            "Shotgun": [],
            "Sniper Rifle": [],
            "Fusion Rifle": [],
            "Grenade Launcher": [],
            "Rocket Launcher": [],
            "Linear Fusion Rifle": [],
            "Machine Gun": [],
            "Sword": []
            }
        }

    #the part of code that works the magic: actually not that bad
    #all it does is check if the catagory name is in the bounty requirements
    #and if it is, add it to that catagory
    #not foolproof, but it'll do for now
    for catagory in bountyCatagories:
        for value in bountyCatagories[catagory]:
            if(value == "Strikes"):
                for bountyName in vendors["Commander Zavala"]["bounties"]:
                    bountyCatagories[catagory][value].append(bountyName)
            else:
                for vendor in vendors:
                    for bountyName in vendors[vendor]["bounties"]:
                        if(value in vendors[vendor]["bounties"][bountyName]):
                            bountyCatagories[catagory][value].append(bountyName)
    return bountyCatagories