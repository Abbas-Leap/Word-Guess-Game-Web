activeUsers = []
readyUsers = []


# Ready
def addUserToReady(username):
    readyUsers.append(username)
    return {"status": "ok"}


def removeUserFromReady(username):
    if username not in activeUsers:
        return {"status": "declined"}

    readyUsers.remove(username)
    return {"status": "ok"}


def getReadyUsers() -> dict:
    return {"status": "ok", "data": readyUsers}


# Active / Online
def addUserToActive(username):
    activeUsers.append(username)
    return {"status": "ok"}


def removeUserFromActive(username):
    activeUsers.remove(username)
    readyUsers.remove(username)
    return {"status": "ok"}


def getActiveUsers() -> dict:
    return {"status": "ok", "data": activeUsers}
