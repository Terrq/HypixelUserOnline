### Modules ###

import requests
import time
from datetime import datetime

### Global Variables ###

apiKey = "<YOUR API KEY>" # Replace with your own Hypixel API key (found by doing /api when logged in to hypixel)
ign = input("Enter the users IGN: ") # Input for IGN

### Functions ###

def getUUID(ign): # Function to get a users UUID from their IGN

    mojangURL = "https://api.mojang.com/users/profiles/minecraft/" + ign # Opens Mojang API with requests

    mojangPage = requests.get(mojangURL)
    mojangContent = mojangPage.text

    findUUID = "id"
    lenFind = len(findUUID)
    lenUUID = 32

    startFind = mojangContent.find(findUUID)+lenFind+3
    extractedUUID = mojangContent[startFind:startFind+lenUUID] # Extracts UUID from Mojang API

    return(extractedUUID) # Returns UUID


def onlineCheck(uuid): # Function to check if a UUID is online

    URL = "https://api.hypixel.net/player?key="+apiKey+"&uuid="+uuid # Opens Hypixel API with requests

    page = requests.get(URL)
    content = page.text

    findLogin = "lastLogin"
    findLogout = "lastLogout"


    len1 = len(findLogin)
    len2 = len(findLogout)

    startLogin = content.find(findLogin)+len1+2
    startLogout = content.find(findLogout)+len2+2

    extractedLogin = content[startLogin:startLogin+13] # Stores last login
    extractedLogout = content[startLogout:startLogout+13] # Stores last logout

    logoutInt = int(extractedLogout)

    if extractedLogin > extractedLogout: # Checks a user is online
        return("Online")
    else:
        return("Last Logout: " + datetime.utcfromtimestamp(logoutInt/1000).strftime('%d-%m-%Y %H:%M:%S')) # Converts unix time to readable date

### Main Script ###

uuid = getUUID(ign) # Saves UUID to a variable
while True: # Infinite loop that runs the check function every second
    check = (onlineCheck(uuid))
    time.sleep(1) # Limited to 1 second so API key does not get blocked
    print(check) # Probably not needed
    while check == "Online":
        check = (onlineCheck(uuid))
        time.sleep(1)
    print(check) # Probably not needed
    while check != "Online":
        check = (onlineCheck(uuid))
        time.sleep(1)

