from pathlib import Path
from time import sleep

from flask import Flask, Response, json, jsonify, render_template, stream_with_context
from flask.globals import request
from flask.helpers import make_response, url_for
from werkzeug.utils import redirect

import CONSTANTS
from dataBase import api as dataBaseAPI
from features.chat import api as chatAPI
from features.game import api as gameAPI
from features.lobby import api as lobbyAPI
from features.login import api as loginAPI
from features.users import api as usersTrackAPI
from logs import api as lg

app = Flask(__name__)

htmlTemplates = Path(__file__).resolve().parent / "templates"


@app.route("/")
def index():
    resp = make_response(redirect(url_for("login")))

    for i, v in request.cookies.items():
        resp.delete_cookie(key=i)
    return resp


@app.route("/login")
def login():
    # If there are cookies reset them
    if "username" in request.cookies:
        return redirect(url_for("index"))
    #
    return render_template("login.html")


@app.route("/loginComms", methods=["POST", "GET"])
def loginComms():
    loginData = request.get_json()
    #
    isLoginDataValid = loginAPI.validateInput(
        username=loginData["username"], password=loginData["password"]
    )

    if isLoginDataValid["status"] == "declined":
        return jsonify(isLoginDataValid)
    # If username not found
    if loginAPI.findUsername(username=loginData["username"])["status"] == "failed":
        dataBaseAPI.createAccount(
            username=loginData["username"], password=loginData["password"]
        )

        return jsonify(
            {
                "status": "createdAccount",
                "msg": "Created a new account please reenter all your login data to login",
            }
        )
    # If username found
    isLoginDataCorrect = loginAPI.verifyLoginDataCorrect(
        username=loginData["username"], password=loginData["password"]
    )

    if isLoginDataCorrect["status"] == "mismatch":
        return jsonify({"status": "declined", "msg": isLoginDataCorrect["msg"]})
    # If account already active
    if loginData["username"] in usersTrackAPI.getActiveUsers():
        return jsonify({"status": "declined", "msg": "Account already active"})
    # If everything matches all inputs valid username found password matches
    finalResp = make_response(
        jsonify(
            {
                "status": "ok",
                "msg": "Succesfully logged in",
                "subLink": url_for("lobbyPage"),
            }
        )
    )
    finalResp.set_cookie("username", loginData["username"])

    usersTrackAPI.addUserToActive(loginData["username"])

    return finalResp


@app.route("/lobby")
def lobbyPage():
    if "username" not in request.cookies.keys():
        lg.logInfo("Username not found")
        return redirect(url_for("index"))
    #
    if request.cookies.get("username") not in usersTrackAPI.getActiveUsers():
        lg.logInfo(
            f"Possible back door from {request.cookies.get('username')} got kicked"
        )
        return redirect(url_for("index"))
    #

    return render_template("lobby.html")


@app.route("/lobbyOneTimeComm", methods=["POST", "GET"])
def lobbyOneTimeComm():
    # User Info
    username = request.cookies.get("username")
    accountInfo = dataBaseAPI.fetchAllAccountData(username=username)

    points = accountInfo["data"][2]
    # Players Info
    numOfActiveUsers = len(usersTrackAPI.getActiveUsers())
    numOfReadyUsers = len(usersTrackAPI.getReadyUsers())
    # Send
    return jsonify(
        {
            "status": "ok",
            "data": {
                "username": username,
                "points": points,
                "numOfActiveUsers": numOfActiveUsers,
                "numOfReadyUsers": numOfReadyUsers,
                "chatHistory": chatAPI.getChatHistory(),
            },
        }
    )


@app.route("/lobbyUsersStatusComm", methods=["GET", "POST"])
def lobbyUsersStatusComm():
    return Response(
        stream_with_context(
            lobbyAPI.getUserStatusGenerator(request.cookies.get("username"))
        ),
        mimetype="text/event-stream",
    )


@app.route("/lobbyReadyComm", methods=["POST", "GET"])
def lobbyReadyComm():

    newState = ""

    print("ReadyToggle")
    # Security
    if request.cookies.get("username") not in usersTrackAPI.getActiveUsers():
        return jsonify({"status": "declined"})

    # Un ready
    if request.cookies.get("username") in usersTrackAPI.getReadyUsers():
        usersTrackAPI.removeUserFromReady(request.cookies.get("username"))
        lg.logInfo(f"{request.cookies.get('username')} Unready")
        newState = "Unready"
    else:  # Ready
        usersTrackAPI.addUserToReady(request.cookies.get("username"))
        lg.logInfo(f"{request.cookies.get('username')} Ready")
        newState = "Ready"
    # Game start
    if (
        len(usersTrackAPI.getReadyUsers()) == len(usersTrackAPI.getActiveUsers())
        and len(usersTrackAPI.getActiveUsers()) >= CONSTANTS.minNumOfPlayers
    ):
        gameAPI.startGame()
    #
    return jsonify({"status": "ok", "newState": newState})


@app.route("/chatSendComm", methods=["POST", "GET"])
def chatComm():
    message = request.get_json()["message"]
    # Format
    finalMessage = f"{request.cookies.get('username')}: {message}"
    # Send
    chatAPI.sendMessage(finalMessage)
    #
    return ""


@app.route("/game")
def game():
    return "Game"


if __name__ == "__main__":
    app.run()
