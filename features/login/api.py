from dataBase import api as dataBaseAPI
from logs import api as lg


def validateInput(username, password):
    usernameRes = dataBaseAPI.validateUsername(username=username)
    #
    passwordRes = {}

    if len(password) < 3:
        passwordRes["status"] = "declined"
        passwordRes["msg"] = "Password too short"
    else:
        passwordRes["status"] = "ok"
    #
    if usernameRes["status"] == "declined":
        return usernameRes

    elif passwordRes["status"] == "declined":
        return passwordRes

    return {"status": "ok"}


def findUsername(username):
    result = dataBaseAPI.fetchAllAccountData(username=username)

    return {"status": result["status"]}
