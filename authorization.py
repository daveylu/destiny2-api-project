import requests

"""
File Description: This file contains the information and various things needed for
authorization of API usage as well as for players to allow access of their account to this app.
"""

#info
clientID = "36124"
# copy-paste myAuthorizeURL into browser, and get authorizeToken from redirectURL
rootPath = "https://www.bungie.net/Platform"
myAuthorizeURL = "https://www.bungie.net/en/oauth/authorize?client_id=36124&response_type=code&state=yay15112&reauth=true"
redirectURL = "https://www.google.com/"
tokenURL = "https://www.bungie.net/Platform/App/OAuth/token/"


authorizeToken = "a6cd3875f88c547602ca82d504a5844c"
accessToken = "COmZAxKGAgAgy4uRPdUdUxk79Wd4cUnG8DCzKaczENMiTXHGrFtN0q/gAAAAKJJOaoJELqWLOrvdQrQgRZ9CoB+ESmmP6qQacLUSnBfJzcTPLwMM42C4E+FuJ0o8ldtbAKda1zssH+Z5oc8WgoFhXRlMmYFQBSOsKTZrchbUF8mrlBl1KjxM1nlX3WQXbne+PiEzNdpZ0uIBl04O+IbG+UbOF0CZxuXlNl8X+Rjukm8UX8C8ZSv6ApBngni6RDMnm5DBfQpzpjhLrIZKoO2wZY879TyrgaowJ/BTaQIyZIryl+oZaoJsJBPg6zCT90bykJY/tfrBbG2Ja0GEb1fA0aXMwgtZnWDpF5TdlzI="

#headers that need to be passed in for the API to be usable
headers = {
    "X-API-Key":'c75b62a96f25471f8195b854e5f31e2c',
    "Authorization": f"Bearer {accessToken}"
}

#headers that need to be passed in during the Authorization portion in order to be authorized
accessTokenData = {
    "grant_type": "authorization_code",
    "code": authorizeToken,
    "client_id": clientID
}

#test function to see if I have access to protected data
def authenticated():
    r = requests.get(rootPath + "/User/GetMembershipsForCurrentUser/", headers = headers)
    try:
        response = r.json()
        return response["ErrorStatus"] == "Success"
    except:
        return False

# # used to get the accessToken maunually for testing, uncomment this section when you need to refresh the accessToken
# response = requests.post("https://www.bungie.net/Platform/App/OAuth/token/", data=accessTokenData)
# response = response.json()
# print("\""+ response["access_token"] + "\"")