from pathlib import Path

from flask import Flask, jsonify, render_template
from flask.globals import request
from flask.helpers import make_response, url_for
from werkzeug.utils import redirect

from dataBase import api as dataBaseAPI
from features.game import api as gameAPI
from features.login import api as loginAPI
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

    return finalResp


@app.route("/lobby")
def lobbyPage():
    htmlCode = ""

    with open(htmlTemplates / "lobby.html", "r") as f:
        htmlCode = f.read()

    accountInfo = dataBaseAPI.fetchAllAccountData(request.cookies.get("username"))

    return (
        htmlCode.replace("PLAYERUSERNAME", str(accountInfo["data"][0]))
        .replace("PLAYERPOINTS", str(accountInfo["data"][2]))
        .replace("NUMBEROFACTIVEPLAYERS", str(5))
        .replace("NUMBEROFREADYPLAYERS", str(0))
    )
