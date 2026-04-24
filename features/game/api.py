import random

playerIds = []

wordInfo = {"word": "", "size": 0}


def addPlayerId(id):
    if id in playerIds:
        return {"status": "declined", "nextId": playerIds[len(playerIds) - 1] + 1}

    playerIds.append(id)

    return {"status": "ok"}


def removePlayerId(id):
    if id not in playerIds:
        return {"status": "declined", "msg": "not found"}

    playerIds.remove(id)

    return {"status": "ok"}


def getPlayers():
    return playerIds


def selectAWordSetter():
    players = getPlayers()

    return players[random.randint(0, len(players) - 1)]
