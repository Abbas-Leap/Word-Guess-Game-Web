from features.lobby import api as lobbyAPI

activeUsers = []
readyUsers = []


# Ready
def addUserToReady(username):
    if username in readyUsers:
        return {"status": "declined"}

    readyUsers.append(username)

    lobbyAPI.updateUsersStatus()

    return {"status": "ok"}


def removeUserFromReady(username):
    if username not in activeUsers:
        return {"status": "declined"}

    readyUsers.remove(username)

    lobbyAPI.updateUsersStatus()

    return {"status": "ok"}


def getReadyUsers() -> dict:
    return {"status": "ok", "data": readyUsers}


# Active / Online
def addUserToActive(username):
    if username in activeUsers:
        return {"status": "declined"}

    activeUsers.append(username)

    lobbyAPI.updateUsersStatus()

    return {"status": "ok"}


def removeUserFromActive(username):
    try:
        activeUsers.remove(username)
        readyUsers.remove(username)
    except ValueError:
        pass

    lobbyAPI.updateUsersStatus()

    return {"status": "ok"}


def getActiveUsers() -> dict:
    return {"status": "ok", "data": activeUsers}
