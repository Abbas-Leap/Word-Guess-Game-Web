from flask import Flask
from flask.helpers import url_for
from werkzeug.utils import redirect

from features.game import api as gameAPI

app = Flask(__name__)

print(gameAPI.addPlayerId(1))
print(gameAPI.addPlayerId(2))
print(gameAPI.addPlayerId(3))
print(gameAPI.getPlayers())
print(gameAPI.selectAWordSetter())


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return ""
