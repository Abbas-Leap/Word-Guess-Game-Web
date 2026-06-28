import random

from dataBase import api as dataBaseAPI
from features.users import api as usersTrackAPI

guessers = []

guesserReward = 5
setterReward = 10

runtTimeData = {
    "guessesRemaining": 0,
    "wordSetterUsername": "",
    "currentGuesserIndex": -1,
}

wordInfo = {"word": "", "size": 0}


def resetGameState():
    wordInfo["word"] = ""
    wordInfo["size"] = 0

    runtTimeData["guessesRemaining"] = 0
    runtTimeData["wordSetterUsername"] = ""
    runtTimeData["currentGuesserIndex"] = -1

    guessers.clear()


def getRemainingGuesses():
    return runtTimeData["guessesRemaining"]


def selectAWordSetter():
    players = usersTrackAPI.getPlayers()

    setter = players[random.randint(0, len(players) - 1)]

    runtTimeData["wordSetterUsername"] = setter

    return setter


def setWordAndSetupGame(word: str):
    if len(word) >= 10:
        return {"status": "declined", "msg": "word too long"}

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


def getNextGuesser():
    # If reached end go back to 0
    if runtTimeData["currentGuesserIndex"] == len(guessers) - 1:
        runtTimeData["currentGuesserIndex"] = 0
    else:  # If not 0 go to next
        runtTimeData["currentGuesserIndex"] += 1

    return guessers[runtTimeData["currentGuesserIndex"]]


def getCurrentGuesser():
    if runtTimeData["currentGuesserIndex"] < 0:
        return None
    return guessers[runtTimeData["currentGuesserIndex"]]


def endGame(setterWon):
    if setterWon:
        dataBaseAPI.addPointsToAccount(runtTimeData["wordSetterUsername"], setterReward)
        resetGameState()
        return {"status": "ok"}

    for i in guessers:
        res = dataBaseAPI.addPointsToAccount(i, guesserReward)

        if res["status"] == "declined":
            print("declined")

    resetGameState()
    return {"status": "ok"}
