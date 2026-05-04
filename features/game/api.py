import random

playerUsernames = []

guesserReward = 5
setterReward = 10

runtTimeData = {"guessesRemaining": 0, "wordSetterUsername": ""}

wordInfo = {"word": "", "size": 0}


def addPlayerusername(username):
    if username in playerUsernames:
        return {"status": "declined", "msg": "user already used"}

    playerUsernames.append(username)

    return {"status": "ok"}


def removePlayerusername(username):
    if username not in playerUsernames:
        return {"status": "declined", "msg": "not found"}

    playerUsernames.remove(username)

    return {"status": "ok"}


def resetPlayers():
    playerUsernames.clear()


def getPlayers():
    return playerUsernames


def resetGameState():
    resetPlayers()

    wordInfo["word"] = ""
    wordInfo["size"] = 0

    runtTimeData["guessesRemaining"] = 0
    runtTimeData["wordSetterUsername"] = ""


def getRemainingGuesses():
    return runtTimeData["guessesRemaining"]


def selectAWordSetter():
    players = getPlayers()

    setter = players[random.randint(0, len(players) - 1)]

    runtTimeData["wordSetterUsername"] = setter

    return setter


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
        try:
            if (
                guess[i] == wordInfo["word"][i]
                and wordInfo["word"].count(guess[i]) > lettersInfoRunTime[guess[i]]
            ):
                letterFeedBack.append("g")
                lettersInfoRunTime[guess[i]] += 1
                continue

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


def isGuessCorrect(letterFeedBack):
    if letterFeedBack.count("g") == len(letterFeedBack):
        return True

    return False
