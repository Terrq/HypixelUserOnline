### Modules ###

import requests
import time
from datetime import datetime

### Global Variables ###

apiKey = "<YOUR API KEY>" # Replace with your own Hypixel API key (found by doing /api when logged in to hypixel)
ign = input("Enter the users IGN: ") # Input for IGN
now = datetime.now()
currentTime = now.strftime("%H:%M:%S")

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

    loginInt = int(extractedLogin) # Stores last login as an integer
    logoutInt = int(extractedLogout) # Stores last logout as an integer
    
    now = datetime.now() 
    currentTime = now.strftime("%H:%M:%S") # Generates a live timestamp
    
    if extractedLogin > extractedLogout: # Checks a user is online
        return(currentTime+": Online (Joined " + datetime.utcfromtimestamp(loginInt/1000).strftime("%H:%M:%S") + ")") 
    else:
        return(currentTime+": Offline (Last seen " + datetime.utcfromtimestamp(logoutInt/1000).strftime("%d-%m-%Y %H:%M:%S") + ")") # Converts unix time to readable date

### Main Script ###

uuid = getUUID(ign) # Saves UUID to a variable
while True: # Infinite loop that runs the check function every second
    check = (onlineCheck(uuid))
    time.sleep(1) # Limited to 1 second so API key does not get blocked
    print(check) # Probably not needed
    while len(check) == 49:
        check = (onlineCheck(uuid))
        time.sleep(1)
    print(check) # Probably not needed
    while len(check) != 49:
        check = (onlineCheck(uuid))
        time.sleep(1)

