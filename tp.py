import requests
import random
import authorization
from cmu_112_graphics import *
from bounties import *
from playerInfo import *
from playerWeaponInfo import *
from weaponSuggestions import *
from graphing import *
from pgcrDataCollection import *

"""
Requests module Documentation: https://docs.python-requests.org/en/master/
Where I got a crash course on the Requests module: https://www.dataquest.io/blog/python-api-tutorial/

Bungie.net API Documentation: https://bungie-net.github.io/multi/index.html

Destiny Data Explorer: https://data.destinysets.com/api
    Used to test API endpoints without actually having to write code (goddamn is this helpful)

Bungie.net Oauth2 Tutorial/Demo: https://lowlidev.com.au/destiny/authentication-2

All images taken directly from Bungie at https://www.bungie.net/

Information about shields and enemy types taken from: https://docs.google.com/spreadsheets/d/1tB87AL467rpjsIAe6PkMdVI3hHQ9rGFbcwQCDCACRZI/htmlview#]

For clearer documentation on unlisted functions, go to the other files within the folder to see their code.
"""

#some global variables
rootPath = "https://www.bungie.net/Platform"

"""
Extra information:
loginURL = "https://tinyurl.com/1511Destiny2"
tokenURL = "https://www.bungie.net/Platform/App/OAuth/token/"
clientID = 36124
myAuthorizeURL = "https://www.bungie.net/en/oauth/authorize?client_id=36124&response_type=code&state=yay15112&reauth=true"
redirectURL = "https://www.google.com/"
"""

def appStarted(app):
    app.mode = "authorization"
    app.time = None

def authorization_keyPressed(app, event):
    code = None
    code = app.getUserInput('What is the URL?')
    if(code == None):
        appStarted(app)
    else:
        authorization.accessTokenData["code"] = code[29:61]
        response = requests.post("https://www.bungie.net/Platform/App/OAuth/token/", data=authorization.accessTokenData)
        response = response.json()
        accessToken = response["access_token"]
        authorization.headers["Authorization"] = f"Bearer {accessToken}"
        if(authorization.authenticated() == True):
            app.mode = "authorizationSuccess"
            app.time = time.time()
        else:
            appStarted(app)

def authorization_redrawAll(app, canvas):
    canvas.create_text(app.width//2, app.height*1//3, text = "https://tinyurl.com/1511Destiny2", font = "Arial 16 bold")
    canvas.create_text(app.width//2, app.height*1//3 + 20,
                       text = "Go to the link above and login. Then, after logging in, copy the URL you are redirected to, and paste it into the input box.", font = "Arial 16 bold")
    canvas.create_text(app.width//2, app.height*2//3, text = 'Press any key in order to start inputting your URL!', font = 'Arial 16 bold')
    

def authorizationSuccess_timerFired(app):
    if(time.time() - app.time > 1):
        initializeApp(app)

def authorizationSuccess_redrawAll(app, canvas):
    canvas.create_text(app.width//2, app.height//2, text = "Loading... Please Wait!", font = "Arial 50 bold")
    canvas.create_text(app.width//2, app.height//12, text = "The app may stop responding. Don't worry, that's normal!", font = "Arial 25 bold")

def initializeApp(app):
    app.mode = "start"
    app.activity = None

    #setting some variables once logged in
    app.playerName, app.membershipID, app.membershipType = getPlayerDestinyInfo()
    app.mostUsedWeaponClass, app.mostUsedWeaponClassKills = getMostUsedWeaponClassAccount(app.membershipID, app.membershipType)
    app.characters = getPlayerCharacterInfo(app.membershipID, app.membershipType)
    app.charactersWeaponInfo = []
    app.currCharacter = None
    
    #this section initializes the names of the supported activities
    app.activities = [
        ["Raid", ["Deep Stone Crypt", "Last Wish", "Garden of Salvation"]],
        ["Legendary Lost Sector", ["Exodus Garden 2A", "Veles Labyrinth", "Perdition", "Bunker E15", "Concealed Void",
                                   "K1 Communion", "K1 Logistics", "K1 Crew Quarters", "K1 Revelations"]],
        ["Nightfall", ["Devil's Lair", "Arms Dealer", "Proving Grounds", "Warden of Nothing", "Fallen SABER", "The Insight Terminus"]],
        ["Dungeon", ["Shattered Throne", "Pit of Heresy", "Prophecy"]],
        ["Empire Hunt", ["The Technocrat", "The Warrior", "The Dark Priestess"]],
        ["Gambit", []]
    ]

    #this section create entries in each character's dictionary for things documented below
    for characterID in app.characters:

        #this part finds the currently equipped weapons and loads their icon images
        app.characters[characterID]["equippedWeapons"] = getEquippedWeaponsCharacter(app.membershipID, app.membershipType, characterID)
        for weaponType in app.characters[characterID]["equippedWeapons"]:
            weaponIconImage = app.loadImage("https://www.bungie.net" + app.characters[characterID]["equippedWeapons"][weaponType]["weaponIconURL"])
            app.characters[characterID]["equippedWeapons"][weaponType]["weaponIconImage"] = weaponIconImage

        #this part finds each character's most exotic weapon, and loads the icon image for it
        bestExoticID, exoticWeaponName, exoticWeaponKills = getMostUsedExoticWeaponCharacter(app.membershipID, app.membershipType, characterID)
        emblemImage = app.loadImage("https://www.bungie.net" + app.characters[characterID]["emblemPath"])
        app.characters[characterID]["bestExoticID"] = bestExoticID
        app.characters[characterID]["exoticWeaponName"] = exoticWeaponName
        app.characters[characterID]["exoticWeaponKills"] = exoticWeaponKills
        app.characters[characterID]["emblemImage"] = emblemImage
        response = requests.get(rootPath + f"/Destiny2/Manifest/DestinyInventoryItemDefinition/{bestExoticID}/", headers = headers)
        response = response.json()
        weaponIconURL = response["Response"]["displayProperties"]["icon"]
        weaponIconImage = app.loadImage("https://www.bungie.net" + weaponIconURL)
        app.characters[characterID]["exoticWeaponIconImage"] = weaponIconImage

def start_keyPressed(app, event):
    app.mode = "characterSelection"

def start_mousePressed(app, event):
    if(event.y >= app.height*10//12):
        if(event.x <= app.width//2):
            app.mode = "characterSelection"
            app.afterLoad = "raidStats"
        else:
            app.mode = "characterSelection"
            app.afterLoad = "pickYourPoison"

def start_redrawAll(app, canvas):
    canvas.create_text(app.width//2, app.height//10, text="Username: " + app.playerName, font = "Arial 20 bold")
    canvas.create_text(app.width//2, app.height*2//10, text ="Most used weapon class: " + app.mostUsedWeaponClass, font = "Arial 20 bold")
    canvas.create_text(app.width//4, app.height*10//12, text = "For more stats, click here!", font = "Arial 25 bold", anchor = "n")
    canvas.create_text(app.width*3//4, app.height*10//12, text = "For bounties and suggestions, click here!", font = "Arial 25 bold", anchor = "n")
    drawCharacterInfo(app, canvas)

#helper function to draw character stats
def drawCharacterInfo(app, canvas):
    i = 0
    for characterID in app.characters:
        i += 1
        canvas.create_text(app.width*i//4, app.height*3//10, text = app.characters[characterID]["characterClass"], font = "Arial 16 bold")
        canvas.create_image(app.width*i//4, app.height*4//10, image = ImageTk.PhotoImage(app.characters[characterID]["emblemImage"]))
        canvas.create_text(10, app.height*6//10, text = "Most Used Exotic:", font = "Arial 12 bold", anchor = "w")
        canvas.create_text(app.width*i//4, app.height*6//10, text = app.characters[characterID]["exoticWeaponName"], font = "Arial 12 bold")
        canvas.create_image(app.width*i//4, app.height*7//10, image = ImageTk.PhotoImage(app.characters[characterID]["exoticWeaponIconImage"]))
        canvas.create_text(10, app.height*8//10, text = "Number of Kills:", font = "Arial 12 bold", anchor = "w")
        canvas.create_text(app.width*(i)//4, app.height*8//10, text = app.characters[characterID]["exoticWeaponKills"], font = "Arial 12 bold")


def characterSelection_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "start"
    
def characterSelection_mousePressed(app, event):
    characterIDList = list(app.characters.keys())
    if(event.x < app.width*3//8):
        app.currCharacter = characterIDList[0]
    elif(event.x > app.width*5//8):
        app.currCharacter = characterIDList[2]
    else:
        app.currCharacter = characterIDList[1]
    app.loaded = False
    app.mode = "loadingScreen"

def characterSelection_redrawAll(app, canvas):
    canvas.create_text(app.width//2, 0, text = "Select a character", font = "Arial 30 bold", anchor = "n")
    if(app.afterLoad == "pickYourPoison"):
        canvas.create_text(app.width-5, 5,  text = "Weapon Suggestions, Activity Suggestions, and Bounties", font = "Arial 12 bold", anchor = "ne")
    else:
        canvas.create_text(app.width-5, 5, text = "Stats", font = "Arial 12 bold", anchor = "ne")
    i = 0
    for characterID in app.characters:
        i += 1

        canvas.create_text(app.width*i//4, app.height*1//10, text = app.characters[characterID]["characterClass"], font = "Arial 16 bold")
        canvas.create_image(app.width*i//4, app.height*2//10, image = ImageTk.PhotoImage(app.characters[characterID]["emblemImage"]))

        canvas.create_text(10, app.height*3//10, text = "Kinetic Weapon:", font = "Arial 12 bold", anchor = "w")
        canvas.create_text(app.width*i//4, app.height*3//10, text = app.characters[characterID]["equippedWeapons"]["kinetic"]["weaponName"], font = "Arial 12")
        canvas.create_image(app.width*i//4, app.height*4//10, image = ImageTk.PhotoImage(app.characters[characterID]["equippedWeapons"]["kinetic"]["weaponIconImage"]))

        canvas.create_text(10, app.height*5//10, text = "Energy Weapon:", font = "Arial 12 bold", anchor = "w")
        canvas.create_text(app.width*i//4, app.height*5//10, text = app.characters[characterID]["equippedWeapons"]["energy"]["weaponName"], font = "Arial 12")
        canvas.create_image(app.width*i//4, app.height*6//10, image = ImageTk.PhotoImage(app.characters[characterID]["equippedWeapons"]["energy"]["weaponIconImage"]))

        canvas.create_text(10, app.height*7//10, text = "Power Weapon:", font = "Arial 12 bold", anchor = "w")
        canvas.create_text(app.width*i//4, app.height*7//10, text = app.characters[characterID]["equippedWeapons"]["power"]["weaponName"], font = "Arial 12")
        canvas.create_image(app.width*i//4, app.height*8//10, image = ImageTk.PhotoImage(app.characters[characterID]["equippedWeapons"]["power"]["weaponIconImage"]))

#helper function to get the information of your fireteam (including the user)
def getFireteamInfo(app):
    app.fireteam = getPlayerFireteamInfo(app.membershipID, app.membershipType)
    for membershipID in app.fireteam:
        for weaponSlot in app.fireteam[membershipID]["equippedWeapons"]:
            weaponIconURL = app.fireteam[membershipID]["equippedWeapons"][weaponSlot]["weaponIconURL"]
            weaponIconImage = app.loadImage("https://www.bungie.net" + weaponIconURL)
            app.fireteam[membershipID]["equippedWeapons"][weaponSlot]["weaponIconImage"] = weaponIconImage
            emblemPath = app.fireteam[membershipID]["emblemPath"]
            emblemImage = app.loadImage("https://www.bungie.net" + emblemPath)
            app.fireteam[membershipID]["emblemImage"] = emblemImage    

def loadingScreen_timerFired(app):
    if(app.afterLoad == "pickYourPoison"):
        if(app.loaded == False):
            app.catagorizedBounties = catagorizeBounties(app.membershipID, app.membershipType, app.currCharacter)
            app.milestones = getPlayerMilestones(app.membershipID, app.membershipType, app.currCharacter)
            getFireteamInfo(app)
            app.loaded = True
        else:
            app.mode = app.afterLoad
    else:
        if(app.loaded == False):
            app.raidDataPoints = getRaidDataPoints(app.membershipID, app.membershipType, app.currCharacter)
            app.strikeDataPoints = getStrikeDataPoints(app.membershipID, app.membershipType, app.currCharacter)
            app.nightfallLLSDataPoints = getNightfallLLSDataPoints(app.membershipID, app.membershipType, app.currCharacter)
            app.gambitDataPoints = getGambitDataPoints(app.membershipID, app.membershipType, app.currCharacter)
            app.dungeonDataPoints = getDungeonDataPoints(app.membershipID, app.membershipType, app.currCharacter)
            app.loaded = True
        else:
            app.mode = app.afterLoad

def loadingScreen_redrawAll(app, canvas):
    if(app.afterLoad == "pickYourPoison"):
        canvas.create_text(app.width-5, 5, text = "Weapon Suggestions, Activity Suggestions, and Bounties", font = "Arial 12 bold", anchor = "ne")
    else:
        canvas.create_text(app.width-5, 5, text = "Stats", font = "Arial 12 bold", anchor = "ne")
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    characterClass = app.characters[app.currCharacter]["characterClass"]
    canvas.create_text(app.width//2, app.height//3, text = f"Loading your {characterClass}... Please Wait!", font = "Arial 60 bold")
    canvas.create_text(app.width//2, app.height*2//3, text = "The app may stop responding. It just takes a long time to load, so don't worry!", font = "Arial 30 bold")

#helper functions to get information about previously completed raids, and convert it into usable data points
def getRaidDataPoints(membershipID, membershipType, characterID):
    raidData = raidActivityHistory(membershipID, membershipType, characterID)
    raidTimePlayedPoints = []
    raidOpponentsDefeatedPoints = []
    raidDeathsPoints = []
    raidEfficiencyPoints = []
    numOfPoints = len(raidData)
    mostTimePlayed = -1
    mostOpponentsDefeated = -1
    mostDeaths = -1
    mostEfficiency = -1
    for i in range(numOfPoints):
        if(raidData[i]["completionReason"] == 0):
            value = True
        else:
            value = False
        
        timePlayed = raidData[i]["timePlayed"]
        if(timePlayed > mostTimePlayed):
            mostTimePlayed = timePlayed
        raidTimePlayedPoints.append((i + 1, timePlayed, value))

        opponentsDefeated = raidData[i]["opponentsDefeated"]
        if(opponentsDefeated > mostOpponentsDefeated):
            mostOpponentsDefeated = opponentsDefeated
        raidOpponentsDefeatedPoints.append((i + 1, opponentsDefeated, value))

        deaths = raidData[i]["deaths"]
        if(deaths > mostDeaths):
            mostDeaths = deaths
        raidDeathsPoints.append((i + 1, deaths, value))

        efficiency = raidData[i]["efficiency"]
        if(efficiency > mostEfficiency):
            mostEfficiency = efficiency
        raidEfficiencyPoints.append((i + 1, efficiency, value))

    return {"raidTimePlayedPoints": raidTimePlayedPoints, "raidOpponentsDefeatedPoints": raidOpponentsDefeatedPoints,
            "raidDeathsPoints": raidDeathsPoints, "raidEfficiencyPoints": raidEfficiencyPoints,
            "numOfPoints": numOfPoints, "mostTimePlayed": mostTimePlayed, "mostOpponentsDefeated": mostOpponentsDefeated, "mostDeaths": mostDeaths, "mostEfficiency": mostEfficiency}

#helper functions to get information about previously completed strikes, and convert it into usable data points
def getStrikeDataPoints(membershipID, membershipType, characterID):
    strikeData = strikeActivityHistory(membershipID, membershipType, characterID)
    strikeTimePlayedPoints = []
    strikeOpponentsDefeatedPoints = []
    strikeDeathsPoints = []
    strikeEfficiencyPoints = []
    numOfPoints = len(strikeData)
    mostTimePlayed = -1
    mostOpponentsDefeated = -1
    mostDeaths = -1
    mostEfficiency = -1

    for i in range(numOfPoints):
        if(strikeData[i]["completionReason"] == 0):
            value = True
        else:
            value = False
        
        timePlayed = strikeData[i]["timePlayed"]
        if(timePlayed > mostTimePlayed):
            mostTimePlayed = timePlayed
        strikeTimePlayedPoints.append((i + 1, timePlayed, value))

        opponentsDefeated = strikeData[i]["opponentsDefeated"]
        if(opponentsDefeated > mostOpponentsDefeated):
            mostOpponentsDefeated = opponentsDefeated
        strikeOpponentsDefeatedPoints.append((i + 1, opponentsDefeated, value))

        deaths = strikeData[i]["deaths"]
        if(deaths > mostDeaths):
            mostDeaths = deaths
        strikeDeathsPoints.append((i + 1, deaths, value))

        efficiency = strikeData[i]["efficiency"]
        if(efficiency > mostEfficiency):
            mostEfficiency = efficiency
        strikeEfficiencyPoints.append((i + 1, efficiency, value))

    return {"strikeTimePlayedPoints": strikeTimePlayedPoints, "strikeOpponentsDefeatedPoints": strikeOpponentsDefeatedPoints,
            "strikeDeathsPoints": strikeDeathsPoints, "strikeEfficiencyPoints": strikeEfficiencyPoints,
            "numOfPoints": numOfPoints, "mostTimePlayed": mostTimePlayed, "mostOpponentsDefeated": mostOpponentsDefeated, "mostDeaths": mostDeaths, "mostEfficiency": mostEfficiency}
        
#helper functions to get information about previously completed nightfalls + LLS, and convert it into usable data points
def getNightfallLLSDataPoints(membershipID, membershipType, characterID):
    nightfallLLSData = nightfallLLSActivityHistory(membershipID, membershipType, characterID)
    nightfallData = nightfallLLSData[0]
    llsData = nightfallLLSData[1]

    nightfallTimePlayedPoints = []
    nightfallOpponentsDefeatedPoints = []
    nightfallDeathsPoints = []
    nightfallEfficiencyPoints = []
    nightfallYourScorePoints = []
    nightfallTeamScorePoints = []
    numOfNightfallPoints = len(nightfallData)
    mostNightfallTimePlayed = -1
    mostNightfallOpponentsDefeated = -1
    mostNightfallDeaths = -1
    mostNightfallEfficiency = -1
    mostNightfallYourScore = -1
    mostNightfallTeamScore = -1
    
    for i in range(numOfNightfallPoints):
        if(nightfallData[i]["completionReason"] == 0):
            value = True
        else:
            value = False

        nightfallTimePlayed = nightfallData[i]["timePlayed"]
        if(nightfallTimePlayed > mostNightfallTimePlayed):
            mostNightfallTimePlayed = nightfallTimePlayed
        nightfallTimePlayedPoints.append((i + 1, nightfallTimePlayed, value))

        nightfallOpponentsDefeated = nightfallData[i]["opponentsDefeated"]
        if(nightfallOpponentsDefeated > mostNightfallOpponentsDefeated):
            mostNightfallOpponentsDefeated = nightfallOpponentsDefeated
        nightfallOpponentsDefeatedPoints.append((i + 1, nightfallOpponentsDefeated, value))

        nightfallDeaths = nightfallData[i]["deaths"]
        if(nightfallDeaths > mostNightfallDeaths):
            mostNightfallDeaths = nightfallDeaths
        nightfallDeathsPoints.append((i + 1, nightfallDeaths, value))

        nightfallEfficiency = nightfallData[i]["efficiency"]
        if(nightfallEfficiency > mostNightfallEfficiency):
            mostNightfallEfficiency = nightfallEfficiency
        nightfallEfficiencyPoints.append((i + 1, nightfallEfficiency, value))

        nightfallYourScore = nightfallData[i]["yourScore"]
        if(nightfallYourScore > mostNightfallYourScore):
            mostNightfallYourScore = nightfallYourScore
        nightfallYourScorePoints.append((i + 1, nightfallYourScore, value))

        nightfallTeamScore = nightfallData[i]["teamScore"]
        if(nightfallTeamScore > mostNightfallTeamScore):
            mostNightfallTeamScore = nightfallTeamScore
        nightfallTeamScorePoints.append((i + 1, nightfallTeamScore, value))

    llsTimePlayedPoints = []
    llsOpponentsDefeatedPoints = []
    llsDeathsPoints = []
    llsEfficiencyPoints = []
    llsYourScorePoints = []
    numOfLLSPoints = len(llsData)
    mostLLSTimePlayed = -1
    mostLLSOpponentsDefeated = -1
    mostLLSDeaths = -1
    mostLLSEfficiency = -1
    mostLLSYourScore = -1
    
    for i in range(numOfLLSPoints):
        if(llsData[i]["completionReason"] == 0):
            value = True
        else:
            value = False

        llsTimePlayed = llsData[i]["timePlayed"]
        if(llsTimePlayed > mostLLSTimePlayed):
            mostLLSTimePlayed = llsTimePlayed
        llsTimePlayedPoints.append((i + 1, llsTimePlayed, value))

        llsOpponentsDefeated = llsData[i]["opponentsDefeated"]
        if(llsOpponentsDefeated > mostLLSOpponentsDefeated):
            mostLLSOpponentsDefeated = llsOpponentsDefeated
        llsOpponentsDefeatedPoints.append((i + 1, llsOpponentsDefeated, value))

        llsDeaths = llsData[i]["deaths"]
        if(llsDeaths > mostLLSDeaths):
            mostLLSDeaths = llsDeaths
        llsDeathsPoints.append((i + 1, llsDeaths, value))

        llsEfficiency = llsData[i]["efficiency"]
        if(llsEfficiency > mostLLSEfficiency):
            mostLLSEfficiency = llsEfficiency
        llsEfficiencyPoints.append((i + 1, llsEfficiency, value))

        llsYourScore = llsData[i]["yourScore"]
        if(llsYourScore > mostLLSYourScore):
            mostLLSYourScore = llsYourScore
        llsYourScorePoints.append((i + 1, llsYourScore, value))

    return {"nightfallTimePlayedPoints": nightfallTimePlayedPoints, "nightfallOpponentsDefeatedPoints": nightfallOpponentsDefeatedPoints,
            "nightfallDeathsPoints": nightfallDeathsPoints, "nightfallEfficiencyPoints": nightfallEfficiencyPoints,
            "nightfallYourScorePoints": nightfallYourScorePoints, "nightfallTeamScorePoints": nightfallTeamScorePoints, "numOfNightfallPoints": numOfNightfallPoints,
            "mostNightfallTimePlayed": mostNightfallTimePlayed, "mostNightfallOpponentsDefeated": mostNightfallOpponentsDefeated,
            "mostNightfallDeaths": mostNightfallDeaths, "mostNightfallEfficiency": mostNightfallEfficiency,
            "mostNightfallYourScore": mostNightfallYourScore, "mostNightfallTeamScore": mostNightfallTeamScore,
            "llsTimePlayedPoints": llsTimePlayedPoints, "llsOpponentsDefeatedPoints": llsOpponentsDefeatedPoints,
            "llsDeathsPoints": llsDeathsPoints, "llsEfficiencyPoints": llsEfficiencyPoints,
            "llsYourScorePoints": llsYourScorePoints, "numOfLLSPoints": numOfLLSPoints, 
            "mostLLSTimePlayed": mostLLSTimePlayed, "mostLLSOpponentsDefeated": mostLLSOpponentsDefeated, "mostLLSDeaths": mostLLSDeaths,
            "mostLLSEfficiency": mostLLSEfficiency, "mostLLSYourScore": mostLLSYourScore}

#helper functions to get information about previously completed Gambit matches, and convert it into usable data points
def getGambitDataPoints(membershipID, membershipType, characterID):
    gambitData = gambitActivityHistory(membershipID, membershipType, characterID)

    gambitTimePlayedPoints = []
    gambitOpponentsDefeatedPoints = []
    gambitDeathsPoints = []
    gambitEfficiencyPoints = []
    gambitMotesBankedPoints = []
    numOfPoints = len(gambitData)
    mostTimePlayed = -1
    mostOpponentsDefeated = -1
    mostDeaths = -1
    mostEfficiency = -1
    mostMotesBanked = -1

    for i in range(numOfPoints):
        if(gambitData[i]["standing"] == 0):
            value = True
        else:
            value = False
        
        timePlayed = gambitData[i]["timePlayed"]
        if(timePlayed > mostTimePlayed):
            mostTimePlayed = timePlayed
        gambitTimePlayedPoints.append((i + 1, timePlayed, value))

        opponentsDefeated = gambitData[i]["opponentsDefeated"]
        if(opponentsDefeated > mostOpponentsDefeated):
            mostOpponentsDefeated = opponentsDefeated
        gambitOpponentsDefeatedPoints.append((i + 1, opponentsDefeated, value))

        deaths = gambitData[i]["deaths"]
        if(deaths > mostDeaths):
            mostDeaths = deaths
        gambitDeathsPoints.append((i + 1, deaths, value))

        efficiency = gambitData[i]["efficiency"]
        if(efficiency > mostEfficiency):
            mostEfficiency = efficiency
        gambitEfficiencyPoints.append((i + 1, efficiency, value))

        motesBanked = gambitData[i]["motesBanked"]
        if(motesBanked > mostMotesBanked):
            mostMotesBanked = motesBanked
        gambitMotesBankedPoints.append((i + 1, motesBanked, value))

    return {"gambitTimePlayedPoints": gambitTimePlayedPoints, "gambitOpponentsDefeatedPoints": gambitOpponentsDefeatedPoints,
            "gambitDeathsPoints": gambitDeathsPoints, "gambitEfficiencyPoints": gambitEfficiencyPoints,
            "gambitMotesBankedPoints": gambitMotesBankedPoints, "numOfPoints": numOfPoints, "mostTimePlayed": mostTimePlayed,
            "mostOpponentsDefeated": mostOpponentsDefeated, "mostDeaths": mostDeaths, "mostEfficiency": mostEfficiency, "mostMotesBanked": mostMotesBanked}

#helper functions to get information about previously completed dungeons, and convert it into usable data points
def getDungeonDataPoints(membershipID, membershipType, characterID):
    dungeonData = dungeonActivityHistory(membershipID, membershipType, characterID)
    dungeonTimePlayedPoints = []
    dungeonOpponentsDefeatedPoints = []
    dungeonDeathsPoints = []
    dungeonEfficiencyPoints = []
    numOfPoints = len(dungeonData)
    mostTimePlayed = -1
    mostOpponentsDefeated = -1
    mostDeaths = -1
    mostEfficiency = -1
    for i in range(len(dungeonData)):
        if(dungeonData[i]["completionReason"] == 0):
            value = True
        else:
            value = False
        timePlayed = dungeonData[i]["timePlayed"]
        if(timePlayed > mostTimePlayed):
            mostTimePlayed = timePlayed
        dungeonTimePlayedPoints.append((i + 1, timePlayed, value))

        opponentsDefeated = dungeonData[i]["opponentsDefeated"]
        if(opponentsDefeated > mostOpponentsDefeated):
            mostOpponentsDefeated = opponentsDefeated
        dungeonOpponentsDefeatedPoints.append((i + 1, opponentsDefeated, value))

        deaths = dungeonData[i]["deaths"]
        if(deaths > mostDeaths):
            mostDeaths = deaths
        dungeonDeathsPoints.append((i + 1, deaths, value))

        efficiency = dungeonData[i]["efficiency"]
        if(efficiency > mostEfficiency):
            mostEfficiency = efficiency
        dungeonEfficiencyPoints.append((i + 1, efficiency, value))

    return {"dungeonTimePlayedPoints": dungeonTimePlayedPoints, "dungeonOpponentsDefeatedPoints": dungeonOpponentsDefeatedPoints,
            "dungeonDeathsPoints": dungeonDeathsPoints, "dungeonEfficiencyPoints": dungeonEfficiencyPoints,
            "numOfPoints": numOfPoints, "mostTimePlayed": mostTimePlayed, "mostOpponentsDefeated": mostOpponentsDefeated, "mostDeaths": mostDeaths, "mostEfficiency": mostEfficiency}

def raidStats_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "start"
    else:
        app.mode = "strikeStats"

#info about the graphing function can be found in graphing.py
def raidStats_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    numOfPoints = app.raidDataPoints["numOfPoints"] - 1
    maxTime = app.raidDataPoints["mostTimePlayed"] // 300 * 300
    maxOpponentsDefeated = app.raidDataPoints["mostOpponentsDefeated"] // 50 * 50
    maxDeaths = app.raidDataPoints["mostDeaths"] // 2 * 2
    maxEfficiency = app.raidDataPoints["mostEfficiency"] // 25 * 25
    canvas.create_text(app.width//2, 0, text = "Raids", font = "Arial 40 bold", anchor = "n")
    drawBaseGraph(canvas, app.width//12, app.height//12, app.width//2 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxTime, 1, 300, "Time Played (seconds)")
    drawPoints(canvas, app.width//12, app.height//12, app.width//2 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxTime, 1, 300, app.raidDataPoints["raidTimePlayedPoints"])
    drawBaseGraph(canvas, app.width//2 + 50, app.height//12, app.width*11//12, app.height//2 - 50, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 50, "Opponents Defeated")
    drawPoints(canvas, app.width//2 + 50, app.height//12, app.width*11//12, app.height//2 - 50, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 50, app.raidDataPoints["raidOpponentsDefeatedPoints"])
    drawBaseGraph(canvas, app.width//12, app.height//2 + 50, app.width//2 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, "Deaths")
    drawPoints(canvas, app.width//12, app.height//2 + 50, app.width//2 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, app.raidDataPoints["raidDeathsPoints"])
    drawBaseGraph(canvas, app.width//2 + 50, app.height//2 + 50, app.width*11//12, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 25, "Efficiency")
    drawPoints(canvas, app.width//2 + 50, app.height//2 + 50, app.width*11//12, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 25, app.raidDataPoints["raidEfficiencyPoints"])

def strikeStats_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "start"
    else:
        app.mode = "dungeonStats"

def strikeStats_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    numOfPoints = app.strikeDataPoints["numOfPoints"] - 1
    maxtime = app.strikeDataPoints["mostTimePlayed"] // 120 * 120
    maxOpponentsDefeated = app.strikeDataPoints["mostOpponentsDefeated"] // 25 * 25
    maxDeaths = app.strikeDataPoints["mostDeaths"] // 2 * 2 + 2
    maxEfficiency = app.strikeDataPoints["mostEfficiency"] // 30 * 30
    canvas.create_text(app.width//2, 0, text = "Strikes", font = "Arial 40 bold", anchor = "n")
    drawBaseGraph(canvas, app.width//12, app.height//12, app.width//2 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxtime, 1, 120, "Time Played (seconds)")
    drawPoints(canvas, app.width//12, app.height//12, app.width//2 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxtime, 1, 120, app.strikeDataPoints["strikeTimePlayedPoints"])
    drawBaseGraph(canvas, app.width//2 + 50, app.height//12, app.width*11//12, app.height//2 - 50, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 25, "Opponents Defeated")
    drawPoints(canvas, app.width//2 + 50, app.height//12, app.width*11//12, app.height//2 - 50, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 25, app.strikeDataPoints["strikeOpponentsDefeatedPoints"])
    drawBaseGraph(canvas, app.width//12, app.height//2 + 50, app.width//2 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, "Deaths")
    drawPoints(canvas, app.width//12, app.height//2 + 50, app.width//2 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, app.strikeDataPoints["strikeDeathsPoints"])
    drawBaseGraph(canvas, app.width//2 + 50, app.height//2 + 50, app.width*11//12, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 30, "Efficiency")
    drawPoints(canvas, app.width//2 + 50, app.height//2 + 50, app.width*11//12, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 30, app.strikeDataPoints["strikeEfficiencyPoints"])

def dungeonStats_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "start"
    else:
        app.mode = "gambitStats"

def dungeonStats_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    numOfPoints = app.dungeonDataPoints["numOfPoints"] - 1
    maxtime = app.dungeonDataPoints["mostTimePlayed"] // 120 * 120
    maxOpponentsDefeated = app.dungeonDataPoints["mostOpponentsDefeated"] // 15 * 15
    maxDeaths = app.dungeonDataPoints["mostDeaths"] // 2 * 2 + 2
    maxEfficiency = app.dungeonDataPoints["mostEfficiency"] // 10 * 10
    canvas.create_text(app.width//2, 0, text = "Dungeons", font = "Arial 40 bold", anchor = "n")
    drawBaseGraph(canvas, app.width//12, app.height//12, app.width//2 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxtime, 1, 120, "Time Played (seconds)")
    drawPoints(canvas, app.width//12, app.height//12, app.width//2 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxtime, 1, 120, app.dungeonDataPoints["dungeonTimePlayedPoints"])
    drawBaseGraph(canvas, app.width//2 + 50, app.height//12, app.width*11//12, app.height//2 - 50, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 15, "Opponents Defeated")
    drawPoints(canvas, app.width//2 + 50, app.height//12, app.width*11//12, app.height//2 - 50, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 15, app.dungeonDataPoints["dungeonOpponentsDefeatedPoints"])
    drawBaseGraph(canvas, app.width//12, app.height//2 + 50, app.width//2 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, "Deaths")
    drawPoints(canvas, app.width//12, app.height//2 + 50, app.width//2 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, app.dungeonDataPoints["dungeonDeathsPoints"])
    drawBaseGraph(canvas, app.width//2 + 50, app.height//2 + 50, app.width*11//12, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 10, "Efficiency")
    drawPoints(canvas, app.width//2 + 50, app.height//2 + 50, app.width*11//12, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 10, app.dungeonDataPoints["dungeonEfficiencyPoints"])

def gambitStats_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "start"
    else:
        app.mode = "nightfallStats"

def gambitStats_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    numOfPoints = app.gambitDataPoints["numOfPoints"] - 1
    maxTime = app.gambitDataPoints["mostTimePlayed"] // 120 * 120
    maxOpponentsDefeated = app.gambitDataPoints["mostOpponentsDefeated"] // 5 * 5
    maxDeaths = app.gambitDataPoints["mostDeaths"] // 2 * 2
    maxEfficiency = app.gambitDataPoints["mostEfficiency"] // 5 * 5
    maxMotesBanked = app.gambitDataPoints["mostMotesBanked"] // 10 * 10
    canvas.create_text(app.width//2, 0, text = "Gambit", font = "Arial 40 bold", anchor = "n")
    drawBaseGraph(canvas, app.width//12, app.height//12, app.width//2 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxTime, 1, 120, "Time Played (seconds)")
    drawPoints(canvas, app.width//12, app.height//12, app.width//2 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxTime, 1, 120, app.gambitDataPoints["gambitTimePlayedPoints"])
    drawBaseGraph(canvas, app.width//2 + 50, app.height//12, app.width*11//12, app.height//2 - 50, 0, 0, numOfPoints, maxMotesBanked, 1, 10, "Motes Banked")
    drawPoints(canvas, app.width//2 + 50, app.height//12, app.width*11//12, app.height//2 - 50, 0, 0, numOfPoints, maxMotesBanked, 1, 10, app.gambitDataPoints["gambitMotesBankedPoints"])
    drawBaseGraph(canvas, 50, app.height//2 + 50, app.width//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 5, "Opponents Defeated")
    drawPoints(canvas, 50, app.height//2 + 50, app.width//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 5, app.gambitDataPoints["gambitOpponentsDefeatedPoints"])
    drawBaseGraph(canvas, app.width//3 + 50, app.height//2 + 50, app.width*2//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, "Deaths")
    drawPoints(canvas, app.width//3 + 50, app.height//2 + 50, app.width*2//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, app.gambitDataPoints["gambitDeathsPoints"])
    drawBaseGraph(canvas, app.width*2//3 + 50, app.height//2 + 50, app.width - 50, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 5, "Efficiency")
    drawPoints(canvas, app.width*2//3 + 50, app.height//2 + 50, app.width - 50, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 5, app.gambitDataPoints["gambitEfficiencyPoints"])

def nightfallStats_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "start"
    else:
        app.mode = "llsStats"

def nightfallStats_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    numOfPoints = app.nightfallLLSDataPoints["numOfNightfallPoints"] - 1
    maxTime = app.nightfallLLSDataPoints["mostNightfallTimePlayed"] // 300 * 300
    maxOpponentsDefeated = app.nightfallLLSDataPoints["mostNightfallOpponentsDefeated"] // 10 * 10
    maxDeaths = app.nightfallLLSDataPoints["mostNightfallDeaths"] // 2 * 2
    maxEfficiency = app.nightfallLLSDataPoints["mostNightfallEfficiency"] // 10 * 10
    maxYourScore = app.nightfallLLSDataPoints["mostNightfallYourScore"] // 10000 * 10000
    maxTeamScore = app.nightfallLLSDataPoints["mostNightfallTeamScore"] // 20000 * 20000
    canvas.create_text(app.width//2, 0, text = "Nightfalls", font = "Arial 40 bold", anchor = "n")
    drawBaseGraph(canvas, 50, app.height//12, app.width//3 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxTime, 1, 300, "Time Played (seconds)")
    drawPoints(canvas, 50, app.height//12, app.width//3 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxTime, 1, 300, app.nightfallLLSDataPoints["nightfallTimePlayedPoints"])
    drawBaseGraph(canvas, app.width//3 + 50, app.height//12, app.width*2//3 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxYourScore, 1, 10000, "Your Score")
    drawPoints(canvas, app.width//3 + 50, app.height//12, app.width*2//3 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxYourScore, 1, 10000, app.nightfallLLSDataPoints["nightfallYourScorePoints"])
    drawBaseGraph(canvas, app.width*2//3 + 50, app.height//12, app.width - 50, app.height//2 - 50, 0, 0, numOfPoints, maxTeamScore, 1, 20000, "Team Score")
    drawPoints(canvas, app.width*2//3 + 50, app.height//12, app.width - 50, app.height//2 - 50, 0, 0, numOfPoints, maxTeamScore, 1, 20000, app.nightfallLLSDataPoints["nightfallTeamScorePoints"])
    drawBaseGraph(canvas, 50, app.height//2 + 50, app.width//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 10, "Opponents Defeated")
    drawPoints(canvas, 50, app.height//2 + 50, app.width//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 10, app.nightfallLLSDataPoints["nightfallOpponentsDefeatedPoints"])
    drawBaseGraph(canvas, app.width//3 + 50, app.height//2 + 50, app.width*2//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, "Deaths")
    drawPoints(canvas, app.width//3 + 50, app.height//2 + 50, app.width*2//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, app.nightfallLLSDataPoints["nightfallDeathsPoints"])
    drawBaseGraph(canvas, app.width*2//3 + 50, app.height//2 + 50, app.width - 50, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 10, "Efficiency")
    drawPoints(canvas, app.width*2//3 + 50, app.height//2 + 50, app.width - 50, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 10, app.nightfallLLSDataPoints["nightfallEfficiencyPoints"])

def llsStats_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "start"
    else:
        app.mode = "raidStats"

def llsStats_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    numOfPoints = app.nightfallLLSDataPoints["numOfLLSPoints"] - 1
    maxTime = app.nightfallLLSDataPoints["mostLLSTimePlayed"] // 60 * 60
    maxOpponentsDefeated = app.nightfallLLSDataPoints["mostLLSOpponentsDefeated"] // 10 * 10
    maxDeaths = app.nightfallLLSDataPoints["mostLLSDeaths"] // 2 * 2
    maxEfficiency = app.nightfallLLSDataPoints["mostLLSEfficiency"] // 5 * 5
    maxYourScore = app.nightfallLLSDataPoints["mostLLSYourScore"] // 5000 * 5000
    canvas.create_text(app.width//2, 0, text = "Legendary Lost Sectors", font = "Arial 40 bold", anchor = "n")
    drawBaseGraph(canvas, app.width//12, app.height//12, app.width//2 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxTime, 1, 60, "Time Played (seconds)")
    drawPoints(canvas, app.width//12, app.height//12, app.width//2 - 50, app.height//2 - 50, 0, 0, numOfPoints, maxTime, 1, 60, app.nightfallLLSDataPoints["llsTimePlayedPoints"])
    drawBaseGraph(canvas, app.width//2 + 50, app.height//12, app.width*11//12, app.height//2 - 50, 0, 0, numOfPoints, maxYourScore, 1, 5000, "Score")
    drawPoints(canvas, app.width//2 + 50, app.height//12, app.width*11//12, app.height//2 - 50, 0, 0, numOfPoints, maxYourScore, 1, 5000, app.nightfallLLSDataPoints["llsYourScorePoints"])
    drawBaseGraph(canvas, 50, app.height//2 + 50, app.width//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 10, "Opponents Defeated")
    drawPoints(canvas, 50, app.height//2 + 50, app.width//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxOpponentsDefeated, 1, 10, app.nightfallLLSDataPoints["llsOpponentsDefeatedPoints"])
    drawBaseGraph(canvas, app.width//3 + 50, app.height//2 + 50, app.width*2//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, "Deaths")
    drawPoints(canvas, app.width//3 + 50, app.height//2 + 50, app.width*2//3 - 50, app.height*11//12, 0, 0, numOfPoints, maxDeaths, 1, 1, app.nightfallLLSDataPoints["llsDeathsPoints"])
    drawBaseGraph(canvas, app.width*2//3 + 50, app.height//2 + 50, app.width - 50, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 10, "Efficiency")
    drawPoints(canvas, app.width*2//3 + 50, app.height//2 + 50, app.width - 50, app.height*11//12, 0, 0, numOfPoints, maxEfficiency, 1, 10, app.nightfallLLSDataPoints["llsEfficiencyPoints"])

def pickYourPoison_keyPressed(app, event):
    app.mode = "characterSelection"
    app.loaded = False

def pickYourPoison_mousePressed(app, event):
    if(event.x <= app.width*3//8):
        app.mode = "chooseActivity"
    elif(event.x <= app.width*5//8):
        app.mode = "bountyBoard1"
    else:
        app.mode = "activitySuggestions"

def pickYourPoison_redrawAll(app, canvas):
    canvas.create_text(app.width//2, app.height//5, text = "What do you want to do today?", font = "Arial 40 bold")
    canvas.create_text(app.width//4, app.height//2, text = "Already know what to play", font = "Arial 30 bold")
    canvas.create_text(app.width*2//4, app.height//2, text = "Bounty Board", font = "Arial 30 bold")
    canvas.create_text(app.width*3//4, app.height//2, text = "Activity Suggestions", font = "Arial 30 bold")
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))

def activitySuggestions_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "pickYourPoison"
    else:
        app.mode = "pickForMe"

def activitySuggestions_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//12, text = "Activities To Do This Week", font = "Arial 40 bold")
    canvas.create_text(app.width//2, app.height//12 + 50, text = 'Not sure what to do? Press any key besides "Escape" to let us pick one for you!', font = "Arial 15 bold")
    canvas.create_line(app.width//5 - 50, app.height//7 + 15, app.width*9//10, app.height//7 + 15)
    i = 0
    for milestone in app.milestones:
        i += 1
        canvas.create_text(app.width//5, app.height//7 + i*30, text = milestone, font = "Arial 16 bold", anchor = "w")
        milestoneObjective = app.milestones[milestone]
        canvas.create_text(app.width//2 + 20, app.height//7 + i*30, text = milestoneObjective, font = "Arial 12 bold", anchor = "w")
        canvas.create_line(app.width//5 - 50, app.height//7 + i*30 + 15, app.width*9//10, app.height//7 + i*30 + 15)

    i += 1
    canvas.create_line(app.width//2, app.height//7, app.width//2, app.height//7 + i*30)

def pickForMe_mousePressed(app, event):
    haveNumberOfPlayers = False
    app.givenTime = app.getUserInput("How much time (in minutes) do you have? Please enter a number.")
    if(app.givenTime != None):
        try:
            app.givenTime = int(app.givenTime)
            while(not haveNumberOfPlayers):
                app.numberOfPlayers = app.getUserInput("How many people will be playing, including you? Please enter a number.")
                if(app.numberOfPlayers == "" or app.numberOfPlayers == None):
                    app.showMessage("Please enter a number.")
                    break
                try:
                    app.numberOfPlayers = int(app.numberOfPlayers)
                    haveNumberOfPlayers = True
                    if(event.x <= app.width//2):
                        app.mode = "endgame"
                        app.activity = activity_Endgame(app.givenTime, app.numberOfPlayers)
                    else:
                        app.mode = "casual"
                        app.activity = activity_Casual(app.givenTime, app.numberOfPlayers)
                except:
                    app.showMessage("Please enter a number.")

        except:
            app.showMessage("Please enter a number.")
    else:
        app.showMessage("Please enter a number.")

def pickForMe_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "activitySuggestions"

def pickForMe_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//12, text = "What do you want to do today?", font = "Arial 40 bold")
    canvas.create_text(app.width//3, app.height//2, text = "Endgame PvE", font = "Arial 30 bold")
    canvas.create_text(app.width*2//3, app.height//2, text = "Casual PvE", font = "Arial 30 bold")

def endgame_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "pickForMe"
    else:
        activity = activity_Endgame(app.givenTime, app.numberOfPlayers)
        while(activity == app.activity):
            activity = activity_Endgame(app.givenTime, app.numberOfPlayers)
        app.activity = activity

def endgame_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//12, text = "You could play:", font = "Arial 40 bold")
    canvas.create_text(app.width//2, app.height//2, text = app.activity, font = "Arial 30 bold")
    canvas.create_text(app.width//2, app.height*11//12, text = "Press any key (except Escape) to pick another activity.", font = "Arial 15 bold")

def casual_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "pickForMe"
    else:
        activity = activity_Casual(app.givenTime, app.numberOfPlayers)
        while(activity == app.activity):
            activity = activity_Casual(app.givenTime, app.numberOfPlayers)
        app.activity = activity

def casual_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//12, text = "You could play:", font = "Arial 40 bold")
    canvas.create_text(app.width//2, app.height//2, text = app.activity, font = "Arial 30 bold")
    canvas.create_text(app.width//2, app.height//12 + 50, text = "Press any key (except Escape) to pick another activity.", font = "Arial 15 bold")

#helper function to determine what casual PvE activity to give back, depending on time + number of players
def activity_Casual(time, numberOfPlayers):
    if(numberOfPlayers <= 3):
        activities = ["Gambit", "Battlegrounds", "Vanguard Strikes", "Low Difficulty Nightfalls", "Low Difficulty Nightmare Hunts", "Altars of Sorrow",
                      "Low Difficulty Empire Hunts", "Exo Challenge", "Patrol/Public Events", "Wrathborn Hunts", "Blind Well",
                      "Ascendant Challenge", "Weekly Dreaming City Story Mission"]
    if(numberOfPlayers > 3):
        activities = ["Gambit", "Patrol/Public Events", "Altars of Sorrow", "Blind Well"]

    activity = random.choice(activities)
    return activity

#helper functions to determine what endgame PvE activity to give back, depending on time + number of players
def activity_Endgame(time, numberOfPlayers):
    if(time <= 30):
        if(numberOfPlayers <= 2):
            activities = ["Legendary Lost Sectors", "Gambit"]
        else:
            activities = ["Gambit", "High Difficulty Nightfalls", "High Difficulty Nightmare Hunts", "High Difficulty Empire Hunts", "Harbinger", "Presage"]
    elif(time <= 60):
        if(numberOfPlayers <= 1):
            activities = ["Legendary Lost Sectors", "Gambit"]
        if(numberOfPlayers <= 2):
            activities = ["Legendary Lost Sectors", "Gambit", "Presage", "Harbinger"]
        else:
            activities = ["Gambit", "High Difficulty Nightfalls", "High Difficulty Nightmare Hunts", "High Difficulty Empire Hunts", "Dungeons", "Presage", "Harbinger"]
    else:
        if(numberOfPlayers <= 1):
            activities = ["Legendary Lost Sectors", "Gambit", "Solo Dungeons", "Presage", "Harbinger"]
        elif(numberOfPlayers <= 2):
            activities = ["Legendary Lost Sectors", "Gambit", "Presage", "Harbinger", "Dungeons"]
        elif(numberOfPlayers <= 4):
            activities = ["Gambit", "High Difficulty Nightfalls", "High Difficulty Nightmare Hunts", "High Difficulty Empire Hunts", "Dungeons", "Presage", "Harbinger"]
        else:
            activities = ["Gambit", "High Difficulty Nightfalls", "High Difficulty Nightmare Hunts", "High Difficulty Empire Hunts", "Dungeons", "Raids", "Presage", "Harbinger"]
    
    activity = random.choice(activities)
    return activity

def chooseActivity_keyPressed(app, event):
    app.mode = "pickYourPoison"

def chooseActivity_mousePressed(app, event):
    if(event.x <= app.width*3//8):
        if(event.y < app.height*2//3 - 50):
            app.mode = "raid"
        else:
            app.mode = "dungeon"
    elif(event.x >= app.width*5//8):
        if(event.y < app.height*2//3 - 50):
            app.mode = "nightfall"
        else:
            app.mode = "gambit"
    else:
        if(event.y < app.height*2//3 - 50):
            app.mode = "lls"
        else:
            app.mode = "empireHunt"

def chooseActivity_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//6, text = "Choose Activity", font = "Arial 40 bold")
    for i in range(len(app.activities)):
        catagory = app.activities[i][0]
        j = i + 1
        if(j < 4):
            canvas.create_text(app.width*j//4, app.height//3, text = catagory, font = "Arial 25 bold")
            for a in range(len(app.activities[i][1])):
                activity = app.activities[i][1][a]
                canvas.create_text(app.width*j//4, app.height//3 + 40 + 30*a, text = activity, font = "Arial 15 bold")
        else:
            k = j%4 + 1
            canvas.create_text(app.width*k//4, app.height*2//3, text = catagory, font = "Arial 25 bold")
            for a in range(len(app.activities[i][1])):
                activity = app.activities[i][1][a]
                canvas.create_text(app.width*k//4, app.height*2//3 + 40 + 30*a, text = activity, font = "Arial 15 bold")

def raid_mousePressed(app, event):
    if(event.x <= app.width*3//8):
        app.mode = "deepStoneCrypt"
    elif(event.x <= app.width*5//8):
        app.mode = "lastWish"
    else:
        app.mode = "gardenOfSalvation"

def raid_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "chooseActivity"

def raid_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//6, text = "Raid", font = "Arial 40 bold")
    for i in range(3):
        activityName = app.activities[0][1][i]
        i += 1
        canvas.create_text(app.width*i//4, app.height//2, text = activityName, font = "Arial 30 bold")

def deepStoneCrypt_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "raid"

def deepStoneCrypt_mousePressed(app, event):
    if(event.x <= app.width*3//10):
        app.mode = "cryptSecurity"
    elif(event.x <= app.width*5//10):
        app.mode = "atraks1"
    elif(event.x <= app.width*7//10):
        app.mode = "descent"
    else:
        app.mode = "taniks"

def deepStoneCrypt_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//6, text = "Deep Stone Crypt", font = "Arial 40 bold")
    encounters = ["Crypt Security", "Atraks-1", "Descent", "Taniks, the Abomination"]
    for i in range(len(encounters)):
        j = i + 1
        canvas.create_text(app.width*j//5, app.height//2, text = encounters[i], font = "Arial 25 bold")

def cryptSecurity_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "deepStoneCrypt"

def cryptSecurity_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Crypt Security", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = deepStoneCrypt_CryptSecurity(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def atraks1_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "deepStoneCrypt"

def atraks1_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Atraks-1", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = deepStoneCrypt_Atraks1(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def descent_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "deepStoneCrypt"

def descent_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Descent", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = deepStoneCrypt_Descent(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def taniks_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "deepStoneCrypt"

def taniks_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Taniks, the Abomination", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = deepStoneCrypt_Taniks(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def lastWish_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "raid"

def lastWish_mousePressed(app, event):
    if(event.y <= app.height//2):
        if(event.x <= app.width*3//10):
            app.mode = "kalli"
        elif(event.x <= app.width*5//10):
            app.mode = "shuroChi"
        elif(event.x <= app.width*7//10):
            app.mode = "morgeth"
        else:
            app.mode = "vault"
    else:
        if(event.x <= app.width*3//8):
            app.mode = "rivenCheese"
        elif(event.x <= app.width*5//8):
            app.mode = "rivenLegit"
        else:
            app.mode = "queenswalk"

def lastWish_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//6, text = "Last Wish", font = "Arial 40 bold")
    encounters = ["Kalli", "Shuro Chi", "Morgeth", "Vault", "Riven - Cheese", "Riven - Legit", "Queenswalk"]
    for i in range(len(encounters)):
        encounter = encounters[i]
        i += 1
        if(i < 5):
            canvas.create_text(app.width*i//5, app.height//3, text = encounter, font = "Arial 25 bold")
        else:
            j = i%5 + 1
            canvas.create_text(app.width*j//4, app.height*2//3, text = encounter, font = "Arial 25 bold")

def kalli_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lastWish"

def kalli_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Kalli", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = lastWish_Kalli(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def shuroChi_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lastWish"

def shuroChi_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Shuro Chi", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = lastWish_ShuroChi(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def morgeth_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lastWish"

def morgeth_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Morgeth", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = lastWish_Morgeth(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def vault_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lastWish"

def vault_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Vault", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = lastWish_Vault(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def rivenCheese_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lastWish"

def rivenCheese_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Riven - Cheese", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = lastWish_RivenCheese(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def rivenLegit_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lastWish"

def rivenLegit_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Riven - Legit", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = lastWish_RivenLegit(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def queenswalk_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lastWish"

def queenswalk_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Queenswalk", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = lastWish_Queenswalk(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def gardenOfSalvation_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "raid"

def gardenOfSalvation_mousePressed(app, event):
    if(event.x <= app.width*3//10):
        app.mode = "evade"
    elif(event.x <= app.width*5//10):
        app.mode = "summon"
    elif(event.x <= app.width*7//10):
        app.mode = "consecratedMind"
    else:
        app.mode = "sanctifiedMind"

def gardenOfSalvation_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//6, text = "Garden of Salvation", font = "Arial 40 bold")
    encounters = ["Evade", "Summon", "Consecrated Mind", "Sanctified Mind"]
    for i in range(len(encounters)):
        j = i + 1
        canvas.create_text(app.width*j//5, app.height//2, text = encounters[i], font = "Arial 25 bold")

def evade_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "gardenOfSalvation"

def evade_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Evade", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = gardenOfSalvation_Evade(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def summon_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "gardenOfSalvation"

def summon_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Summon", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = gardenOfSalvation_Summon(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def consecratedMind_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "gardenOfSalvation"

def consecratedMind_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Consecrated Mind", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = gardenOfSalvation_ConsecratedMind(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def sanctifiedMind_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "gardenOfSalvation"

def sanctifiedMind_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Sanctified Mind", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = gardenOfSalvation_SanctifiedMind(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def lls_mousePressed(app, event):
    if(event.y <= app.height//2):
        if(event.x <= app.width*3//12):
            app.mode = "exodusGarden2A"
        elif(event.x <= app.width*5//12):
            app.mode = "velesLabyrinth"
        elif(event.x <= app.width*7//12):
            app.mode = "perdition"
        elif(event.x <= app.width*9//12):
            app.mode = "bunkerE15"
        else:
            app.mode = "concealedVoid"
    else:
        if(event.x <= app.width*3//10):
            app.mode = "k1Communion"
        elif(event.x <= app.width*5//10):
            app.mode = "k1Logistics"
        elif(event.x <= app.width*7//10):
            app.mode = "k1CrewQuarters"
        else:
            app.mode = "k1Revelations"

def lls_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "chooseActivity"

def lls_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//6, text = "Legendary Lost Sector", font = "Arial 40 bold")
    for i in range(9):
        activityName = app.activities[1][1][i]
        i += 1
        if(i < 6):
            canvas.create_text(app.width*i//6, app.height//3, text = activityName, font = "Arial 25 bold")
        else:
            j = i%6 + 1
            canvas.create_text(app.width*j//5, app.height*2//3, text = activityName, font = "Arial 25 bold")

def exodusGarden2A_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lls"

def exodusGarden2A_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Exodus Garden 2A", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = exodusGarden2A()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in [ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def velesLabyrinth_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lls"

def velesLabyrinth_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Veles Labyrinth", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = velesLabyrinth()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in [ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def perdition_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lls"

def perdition_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Perdition", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = perdition()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in [ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def bunkerE15_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lls"

def bunkerE15_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Bunker E15", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = bunkerE15()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in [ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def concealedVoid_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lls"

def concealedVoid_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Concealed Void", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = concealedVoid()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in [ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def k1Communion_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lls"

def k1Communion_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "K1 Communion", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = k1Communion()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in [ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def k1Logistics_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lls"

def k1Logistics_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "K1 Logistics", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = k1Logistics()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in [ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def k1CrewQuarters_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lls"

def k1CrewQuarters_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "K1 Crew Quarters", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = k1CrewQuarters()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in [ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def k1Revelations_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "lls"

def k1Revelations_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "K1 Revelations", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = k1Revelations()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in [ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def nightfall_mousePressed(app, event):
    if(event.y <= app.height//2):
        if(event.x <= app.width*3//8):
            app.mode = "devilsLair"
        elif(event.x <= app.width*5//8):
            app.mode = "armsDealer"
        else:
            app.mode = "provingGrounds"
    else:
        if(event.x <= app.width*3//8):
            app.mode = "wardenOfNothing"
        elif(event.x <= app.width*5//8):
            app.mode = "fallenSaber"
        else:
            app.mode = "insightTerminus"

def nightfall_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "chooseActivity"

def nightfall_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//6, text = "Nightfall", font = "Arial 40 bold")
    for i in range(6):
        activityName = app.activities[2][1][i]
        i += 1
        if(i < 4):
            canvas.create_text(app.width*i//4, app.height//3, text = activityName, font = "Arial 30 bold")
        else:
            j = i%4 + 1
            canvas.create_text(app.width*j//4, app.height*2//3, text = activityName, font = "Arial 30 bold")

def devilsLair_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "nightfall"

def devilsLair_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Devil's Lair", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = devilsLair()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def armsDealer_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "nightfall"

def armsDealer_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Arms Dealer", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = armsDealer()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def provingGrounds_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "nightfall"

def provingGrounds_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Proving Grounds", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = provingGrounds()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def wardenOfNothing_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "nightfall"

def wardenOfNothing_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Warden of Nothing", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = wardenOfNothing()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def fallenSaber_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "nightfall"

def fallenSaber_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Fallen SABER", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = fallenSaber()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def insightTerminus_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "nightfall"

def insightTerminus_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "The Insight Terminus", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = insightTerminus()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def dungeon_mousePressed(app, event):
    if(event.x <= app.width*3//8):
        app.mode = "shatteredThrone"
    elif(event.x <= app.width*5//8):
        app.mode = "pitOfHeresy"
    else:
        app.mode = "prophecy"

def dungeon_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "chooseActivity"

def dungeon_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//6, text = "Dungeon", font = "Arial 40 bold")
    for i in range(3):
        activityName = app.activities[3][1][i]
        i += 1
        canvas.create_text(app.width*i//4, app.height//2, text = activityName, font = "Arial 30 bold")

def shatteredThrone_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "dungeon"

def shatteredThrone_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Shattered Throne", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = shatteredThrone()
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def pitOfHeresy_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "dungeon"

def pitOfHeresy_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Pit of Heresy", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = pitOfHeresy()
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def prophecy_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "dungeon"

def prophecy_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "Prophecy", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = prophecy()
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def empireHunt_mousePressed(app, event):
    if(event.x <= app.width*3//8):
        app.mode = "technocrat"
    elif(event.x <= app.width*5//8):
        app.mode = "warrior"
    else:
        app.mode = "darkPriestess"

def empireHunt_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "chooseActivity"

def empireHunt_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//6, text = "Empire Hunt", font = "Arial 40 bold")
    for i in range(3):
        activityName = app.activities[4][1][i]
        i += 1
        canvas.create_text(app.width*i//4, app.height//2, text = activityName, font = "Arial 30 bold")

def technocrat_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "empireHunt"

def technocrat_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "The Technocrat", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = technocrat()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def warrior_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "empireHunt"

def warrior_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "The Warrior", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = warrior()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def darkPriestess_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "empireHunt"

def darkPriestess_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//15, text = "The Dark Priestess", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Recommendations:", font = "Arial 12 bold", anchor = "w")
    values = darkPriestess()
    shields = "Shields: "
    for element in values["elements"]:
        shields += element + ", "
    shields = shields[:-2]
    canvas.create_text(app.width//2, app.height//15 + 60, text = shields, font = "Arial 15 bold")
    axesNumbers = len(app.fireteam) + 1
    drawFireteam(app, canvas)
    i = 0
    for membershipID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[membershipID]["equippedWeapons"]
        weaponRecommendations = []
        for ammoType in ["primary", "special", "power"]:
            weaponRecommendations += values[ammoType]
        for weaponSlot in equippedWeapons:
            weaponName = equippedWeapons[weaponSlot]["weaponName"]
            weaponType = equippedWeapons[weaponSlot]["weaponType"]
            for ammoType in values:
                if(weaponType in values[ammoType] or weaponName in values[ammoType]):
                    for weapon in values[ammoType]:
                        if(weapon in weaponRecommendations):
                            weaponRecommendations.remove(weapon)
        if(len(weaponRecommendations) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "Prepared!", font = "Arial 12 bold")
        for j in range(len(weaponRecommendations)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = weaponRecommendations[j], font = "Arial 12 bold")

def gambit_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "chooseActivity"

def gambit_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    canvas.create_text(app.width//2, app.height//8, text = "Gambit", font = "Arial 40 bold")
    canvas.create_text(10, app.height*8//10, text = "Roles:", font = "Arial 12 bold", anchor = "w")
    drawFireteam(app, canvas)

    axesNumbers = len(app.fireteam) + 1
    i = 0
    for fireteamMemberID in app.fireteam:
        i += 1
        equippedWeapons = app.fireteam[fireteamMemberID]["equippedWeapons"]
        roles = gambit(equippedWeapons)
        if(len(roles) == 0):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + 20, text = "None!", font = "Arial 12 bold")
        for j in range(len(roles)):
            canvas.create_text(app.width*i//axesNumbers, app.height*8//10 + j*20, text = roles[j], font = "Arial 12 bold")

def drawFireteam(app, canvas):
    axesNumbers = len(app.fireteam) + 1

    i = 0
    for membershipID in app.fireteam:
        i += 1

        canvas.create_text(app.width*i//axesNumbers, app.height*2.5//10 - 60, text = app.fireteam[membershipID]["playerName"], font = "Arial 16 bold")
        canvas.create_image(app.width*i//axesNumbers, app.height*2.5//10, image = ImageTk.PhotoImage(app.fireteam[membershipID]["emblemImage"]))

        canvas.create_text(10, app.height*4//10 - 60, text = "Kinetic Weapon:", font = "Arial 12 bold", anchor = "w")
        canvas.create_text(app.width*i//axesNumbers, app.height*4//10 - 60, text = app.fireteam[membershipID]["equippedWeapons"]["kinetic"]["weaponName"], font = "Arial 12")
        canvas.create_image(app.width*i//axesNumbers, app.height*4//10, image = ImageTk.PhotoImage(app.fireteam[membershipID]["equippedWeapons"]["kinetic"]["weaponIconImage"]))

        canvas.create_text(10, app.height*5.5//10 - 60, text = "Energy Weapon:", font = "Arial 12 bold", anchor = "w")
        canvas.create_text(app.width*i//axesNumbers, app.height*5.5//10 - 60, text = app.fireteam[membershipID]["equippedWeapons"]["energy"]["weaponName"], font = "Arial 12")
        canvas.create_image(app.width*i//axesNumbers, app.height*5.5//10, image = ImageTk.PhotoImage(app.fireteam[membershipID]["equippedWeapons"]["energy"]["weaponIconImage"]))

        canvas.create_text(10, app.height*7//10 - 60, text = "Power Weapon:", font = "Arial 12 bold", anchor = "w")
        canvas.create_text(app.width*i//axesNumbers, app.height*7//10 - 60, text = app.fireteam[membershipID]["equippedWeapons"]["power"]["weaponName"], font = "Arial 12")
        canvas.create_image(app.width*i//axesNumbers, app.height*7//10, image = ImageTk.PhotoImage(app.fireteam[membershipID]["equippedWeapons"]["power"]["weaponIconImage"]))

def bountyBoard1_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "pickYourPoison"
    else:
        app.mode = "bountyBoard2"

def bountyBoard1_mousePressed(app, event):
    app.mode = "bountyBoard2"

def bountyBoard1_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    i = 0
    for bountyCatagory in app.catagorizedBounties["Destination/Activity"]:
        i += 1        
        if(i < 5):
            canvas.create_text(app.width*i//5, app.height//10, text = bountyCatagory, font = "Arial 20 bold")
            a = 1
            for bounty in app.catagorizedBounties["Destination/Activity"][bountyCatagory]:
                a += 1
                canvas.create_text(app.width*i//5, app.height//10 + a*20, text = bounty, font = "Arial 12 bold")
        else:
            j = i%5 + 1
            canvas.create_text(app.width*j//5, app.height//2, text = bountyCatagory, font = "Arial 20 bold")
            b = 1
            for bounty in app.catagorizedBounties["Destination/Activity"][bountyCatagory]:
                b += 1
                canvas.create_text(app.width*j//5, app.height//2 + b*20, text = bounty, font = "Arial 12 bold")

def bountyBoard2_keyPressed(app, event):
    if(event.key == "Escape"):
        app.mode = "pickYourPoison"
    else:
        app.mode = "bountyBoard1"

def bountyBoard2_mousePressed(app, event):
    app.mode = "bountyBoard1"

def bountyBoard2_redrawAll(app, canvas):
    canvas.create_image(50, 50, image = ImageTk.PhotoImage(app.characters[app.currCharacter]["emblemImage"]))
    i = 0
    for weapon in app.catagorizedBounties["Weapon"]:
        i += 1
        if(i < 6):
            canvas.create_text(app.width*i//6, app.height//10, text = weapon, font = "Arial 20 bold")
            if(len(app.catagorizedBounties["Weapon"][weapon]) == 0):
                canvas.create_text(app.width*i//6, app.height//10 + 40, text = "No bounties!", font = "Arial 16 bold")
            else:
                a = 1
                for bounty in app.catagorizedBounties["Weapon"][weapon]:
                    a += 1
                    canvas.create_text(app.width*i//6, app.height//10 + a*20, text = bounty, font = "Arial 12 bold")
        elif(i < 11):
            j = i%5 + 1
            canvas.create_text(app.width*j//6, app.height*4//10, text = weapon, font = "Arial 20 bold")
            if(len(app.catagorizedBounties["Weapon"][weapon]) == 0):
                canvas.create_text(app.width*j//6, app.height*4//10 + 40, text = "No bounties!", font = "Arial 16 bold")
            else:
                b = 1
                for bounty in app.catagorizedBounties["Weapon"][weapon]:
                    b += 1
                    canvas.create_text(app.width*j//6, app.height*4//10 + b*20, text = bounty, font = "Arial 12 bold")
        else:
            k = i%5 + 1
            canvas.create_text(app.width*k//6, app.height*7//10, text = weapon, font = "Arial 20 bold")
            if(len(app.catagorizedBounties["Weapon"][weapon]) == 0):
                canvas.create_text(app.width*k//6, app.height*7//10 + 40, text = "No bounties!", font = "Arial 16 bold")
            else:
                c = 1
                for bounty in app.catagorizedBounties["Weapon"][weapon]:
                    c += 1
                    canvas.create_text(app.width*k//6, app.height*7//10 + c*20, text = bounty, font = "Arial 12 bold")

runApp(width=1920, height=1080)