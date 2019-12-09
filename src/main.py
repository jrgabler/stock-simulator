#!/usr/bin/env python
import os, requests
from flask import Flask, render_template, redirect, url_for
from flask import request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from guppy import hpy

from api import UserService, StockService
from controllers import UserController

# refactor into config.py file
VIEW_DIRECTORY = "./views"
TEMPLATE_FOLDER = os.path.abspath(VIEW_DIRECTORY + "/templates/")
STATIC_FOLDER = os.path.abspath(VIEW_DIRECTORY + "/static/")

# api urls
LOCAL_URL = 'http://localhost:5000'
API_LOGIN = '/login/submit'
API_REGISTER = '/registration'
API_WATCHLIST_ADD = "/watch/add"
API_WATCHLIST_REMOVE = "/watch/remove"

global ACCESS_TOKEN
global REFRESH_TOKEN
ACCESS_TOKEN = ""
REFRESH_TOKEN = ""

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

app.config["JWT_SECRET_KEY"] = "jwt_secret_string"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

blacklist = set()
jwt = JWTManager(app)
api = Api(app)

# guppy
h = hpy()
print(h.heap())

# called every time client tries to access a secure endpoint
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return UserController.tokenIsBlacklisted(jti)


# User Service
api.add_resource(UserService.UserRegistration, API_REGISTER)
api.add_resource(UserService.UserLogin, API_LOGIN)
api.add_resource(UserService.UserLogoutAccess, "/logout/access")
api.add_resource(UserService.UserLogoutRefresh, "/logout/refresh")
api.add_resource(UserService.TokenRefresh, "/token/refresh")
# Stock Service
api.add_resource(StockService.GetStock, "/stock")
api.add_resource(StockService.WatchAsset, API_WATCHLIST_ADD)
api.add_resource(StockService.RemoveWatchedAsset, API_WATCHLIST_REMOVE)


def isLoggedIn(template):
    # if ACCESS_TOKEN or REFRESH_TOKEN:
    return render_template(template)

    # return redirect(url_for('login'))

def get_header(auth_token):
    return {'Authorization': 'Bearer ' + auth_token}

def set_tokens_redirect(json_response, page):
    ACCESS_TOKEN = json_response.get("access_token")
    REFRESH_TOKEN = json_response.get("refresh_token")

    return redirect(url_for(page))

@app.route("/")
@app.route("/home")
def index():
    return isLoggedIn("index.html.j2")

@app.route("/market")
def market():
    return isLoggedIn("market/market.html.j2")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = requests.post(LOCAL_URL + API_LOGIN, data=request.form)
        json_response = response.json()

        if json_response.get("access_token"):
            return set_tokens_redirect(json_response, "index")

            return render_template("login/login.html.j2", error=json_response.get("message"))

    return render_template("login/login.html.j2")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        response = requests.post(LOCAL_URL + API_REGISTER, data=request.form, auth={})
        json_response = response.json()

        if json_response.get("access_token"):
            return set_tokens_redirect(json_response, "login")

        return render_template("login/login.html.j2", error=json_response)

    return render_template("login/register.html.j2")

@app.route("/reset-password")
def reset_password():
    return isLoggedIn("login/password-reset.html.j2")

@app.route("/account")
def account():
    return isLoggedIn("account.html.j2")

@app.route("/stock/purchase")
def stock_purchase():
    return isLoggedIn("stocks/purchase.html.j2")

@app.route("/stock/sell")
def stock_sell():
    return isLoggedIn("stocks/sell.html.j2")

@app.route("/watchlist/manage")
def manage_watchlist():
    return isLoggedIn("watchlist/manage.html.j2")

@app.route("/watchlist/manage", methods=["POST"])
def add_stock_watchlist():
    response = requests.post(LOCAL_URL + API_WATCHLIST_ADD, data=request.form, headers=get_header(ACCESS_TOKEN))
    json_response = response.json()

    # if json_response.get("access_token"):
    #     return set_tokens_redirect(json_response, "manage_watchlist")

    return render_template("watchlist/manage.html.j2", error=json_response.get("message"))

@app.route("/watchlist/manage", methods=["POST"])
def remove_stock_watchlist():
    response = requests.post(LOCAL_URL + API_WATCHLIST_REMOVE, data=request.form, headers=get_header(ACCESS_TOKEN))
    json_response = response.json()

    return render_template("watchlist/manage.html.j2", error=json_response.get("message"))


if __name__ == "__main__":
    app.run(host='0.0.0.0')    # Dockerized
    # app.run(debug=True)    # Debug
