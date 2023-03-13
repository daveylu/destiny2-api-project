import requests
from cmu_112_graphics import *


"""
This file contains the stuff needed for users to login/authenticate,
as well as all of the API stuff needed for calls to work.
"""




#some global variables
rootPath = "https://www.bungie.net/Platform"

"""
tokenURL = "https://www.bungie.net/Platform/App/OAuth/token/"
clientID = 36124
myAuthorizeURL = "https://www.bungie.net/en/oauth/authorize?client_id=36124&response_type=code&state=yay15112&reauth=true"
redirectURL = "https://www.google.com/"
"""


#headers that need to be passed in for the API to be usable
headers = {
    "X-API-Key":'c75b62a96f25471f8195b854e5f31e2c',
    "Authorization": None
}

#headers that need to be passed in during the Authorization portion in order to be authorized
accessTokenData = {
    "grant_type": "authorization_code",
    "code": None,
    "client_id": "36124"
}

#tests if the user has been authenticated
def authenticated():
    r = requests.get(rootPath + "/User/GetMembershipsForCurrentUser/", headers = headers)
    try:
        response = r.json()
        return response["ErrorStatus"] == "Success"
    except:
        return False


def appStarted(app):
    app.mode = "authorization"
    app.authorizeState = False


def authorization_keyPressed(app, event):
    code = None
    code = app.getUserInput('What is the URL?')
    if(code == None):
        appStarted(app)
    else:
        accessTokenData["code"] = code[29:61]
        response = requests.post("https://www.bungie.net/Platform/App/OAuth/token/", data=accessTokenData)
        response = response.json()
        accessToken = response["access_token"]
        headers["Authorization"] = "Bearer " + accessToken
        if(authenticated() == True):
            app.authorizeState = True
            app.mode = "start"
        else:
            appStarted(app)

def authorization_redrawAll(app, canvas):
    if(app.authorizeState == False):
        canvas.create_text(app.width//2, app.height*1//3,
                        text = "https://tinyurl.com/1511Destiny2",
                        font = "Arial 16 bold")
        canvas.create_text(app.width//2, app.height*1//3 + 20,
        text = "Go to the link above and login. Then, after logging in, copy the URL you are redirected to, and paste it into the input box.", font = "Arial 16 bold")
        canvas.create_text(app.width//2, app.height*2//3, text = 'Press any key in order to start inputting your code!',
                        font = 'Arial 16 bold')
    else:
        canvas.create_text(app.width//2, app.height//2, text = "Authorized! Please close the window. The main app will then start running.", font = "Arial 30 bold")


runApp(width=1920, height=1080)