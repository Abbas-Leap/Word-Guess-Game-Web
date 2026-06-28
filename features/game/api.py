import runTime
from features.chat import api as chatAPI
from features.users import api as usersTrackAPI

from . import base


def startGame():
    if runTime.game.onGoing:
        return
    #
    runTime.game.onGoing = True
    # Add cleints to players
    usersTrackAPI.setupPlayers()
    # Send a message to all clients
    chatAPI.sendMessage("Game Started")
