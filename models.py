import os, json, sys, shutil, datetime, time, random, copy

datetimeFormat = "%Y-%m-%d %H:%M:%S"

def fileContent(fileName, passAPIKey=False):
    with open(fileName, "r") as f:
        f_content = f.read()
        if passAPIKey:
            f_content = f_content.replace("\{{ API_KEY }}", os.environ["APIKey"])
            return f_content
        return f_content
    
def generateAuthToken():
    alphanumeric = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    authToken = ""
    for i in range(10):
        authToken += random.choice(alphanumeric)

    return authToken

def expireAuthToken(database):
    tempDatabase = copy.deepcopy(database)
    if "session" in tempDatabase:
        if tempDatabase["session"]["token"] != None:
            if (datetime.datetime.now() -  datetime.datetime.strptime(database["session"]["lastLogin"], datetimeFormat)).total_seconds() > 10800:
                tempDatabase["session"]["token"] = None

    return tempDatabase

def loadFromFile():
    data = {}
    if os.path.isfile(os.path.join(os.getcwd(), "data.txt")):
        with open("data.txt", "r") as f:
            data = json.load(f)
    else:
        with open("data.txt", "w") as f:
            data = {
                "data": {}
            }
            json.dump(data, f)

    return data


def saveToFile(data):
    with open("data.txt", "w") as f:
        json.dump(data, f)