from flask import Flask, render_template
from flask.globals import request
from flask.helpers import make_response, url_for
from werkzeug.utils import redirect

from dataBase import api as dataBaseAPI
from features.game import api as gameAPI
from logs import api as lg

app = Flask(__name__)


@app.route("/")
def index():
    resp = make_response(redirect(url_for("login")))

    for i, v in request.cookies.items():
        resp.delete_cookie(key=i)
    return resp


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/loginComms", methods=["POST", "GET"])
def loginComms():
    return ""
