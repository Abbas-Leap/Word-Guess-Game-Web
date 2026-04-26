import random

playerIds = []

runtTimeData = {"nextId": 0, "guessesRemaining": 0}

wordInfo = {"word": "", "size": 0}


def getAPlayerIdAndAddPlayer():

    playerIds.append(runtTimeData["nextId"])
    runtTimeData["nextId"] += 1

    return {"status": "ok", "nextId": runtTimeData["nextId"]}


def removePlayerId(id):
    if id not in playerIds:
        return {"status": "declined", "msg": "not found"}

    playerIds.remove(id)

    return {"status": "ok"}


def resetPlayers():
    playerIds.clear()


def getPlayers():
    return playerIds


def resetGameState():
    resetPlayers()

    wordInfo["word"] = ""
    wordInfo["size"] = 0

    runtTimeData["guessesRemaining"] = 0
    runtTimeData["nextId"] = 0


def getRemainingGuesses():
    return runtTimeData["guessesRemaining"]


def selectAWordSetter():
    players = getPlayers()

    return players[random.randint(0, len(players) - 1)]


def setWordAndSetupGame(word: str):
    wordInfo["word"] = word.lower()
    wordInfo["size"] = len(word)

    runtTimeData["guessesRemaining"] = len(word) + 1

    return {
        "status": "ok",
        "data": [wordInfo["word"], wordInfo["size"], runtTimeData["guessesRemaining"]],
    }


def makeAGuess(g: str) -> dict:
    if runtTimeData["guessesRemaining"] <= 0:
        return {"status": "declined", "msg": "out of guesses"}

    letterFeedBack = []

    # LettersInfoRunTime basically fixes an issue where
    # the program thinks that a letter has not been seen before (like if letter is typed twice but is only seen once in the word)
    lettersInfoRunTime = {}
    guess = g.lower()

    for i in wordInfo["word"]:
        lettersInfoRunTime[i] = 0

    runtTimeData["guessesRemaining"] -= 1

    for i in range(wordInfo["size"]):
        if (
            guess[i] == wordInfo["word"][i]
            and wordInfo["word"].count(guess[i]) > lettersInfoRunTime[guess[i]]
        ):
            letterFeedBack.append("g")
            lettersInfoRunTime[guess[i]] += 1
            continue

        try:
            if (
                guess[i] in wordInfo["word"]
                and wordInfo["word"].count(guess[i]) > lettersInfoRunTime[guess[i]]
            ):
                letterFeedBack.append("y")
                lettersInfoRunTime[guess[i]] += 1
                continue
        except KeyError:
            pass

        letterFeedBack.append("r")

    return {"status": "ok", "letterFeedBack": letterFeedBack}
