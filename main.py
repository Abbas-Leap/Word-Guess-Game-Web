from flask import Flask
from flask.helpers import url_for
from werkzeug.utils import redirect

from features.game import api as gameAPI

app = Flask(__name__)

print(gameAPI.setWordAndSetupGame("Pops"))
print(gameAPI.makeAGuess("Pops"))
print(gameAPI.makeAGuess("poos"))
print(gameAPI.makeAGuess("lols"))

print(gameAPI.makeAGuess("poos"))
print(gameAPI.makeAGuess("oooo"))
print(gameAPI.makeAGuess("lols"))


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return ""
