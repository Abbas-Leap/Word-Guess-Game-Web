from features.lobby import api as lobbyAPI

chatHistory = []


def getChatHistory():
    return chatHistory


def sendMessage(message):
    chatHistory.append(message)
    lobbyAPI.updateUsersStatus(message=message)
