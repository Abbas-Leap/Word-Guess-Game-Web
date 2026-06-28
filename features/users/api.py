from features.lobby import api as lobbyAPI

activeUsers = []
readyUsers = []
players = []


# Ready
def addUserToReady(username):
    if username in readyUsers:
        return "declined"

    readyUsers.append(username)

    lobbyAPI.updateUsersStatus()

    return "ok"


def removeUserFromReady(username):
    if username not in activeUsers:
        return "declined"

    readyUsers.remove(username)

    lobbyAPI.updateUsersStatus()

    return "ok"


def getReadyUsers() -> list:
    return readyUsers


# Active / Online
def addUserToActive(username):
    if username in activeUsers:
        return "declined"

    activeUsers.append(username)

    lobbyAPI.updateUsersStatus()

    return "ok"


def removeUserFromActive(username):
    try:
        activeUsers.remove(username)
        readyUsers.remove(username)
    except ValueError:
        pass

    lobbyAPI.updateUsersStatus()

    return "ok"


def getActiveUsers() -> list:
    return activeUsers


# Players
def setupPlayers():
    players = activeUsers.copy()


def removePlayer(username):
    if username not in players:
        return "declined"

    players.remove(username)

    return "ok"


def getPlayers() -> list:
    return players
