#!/usr/bin/env python
import os
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
api.add_resource(UserService.UserRegistration, "/registration")
api.add_resource(UserService.UserLogin, "/login")
api.add_resource(UserService.UserLogoutAccess, "/logout/access")
api.add_resource(UserService.UserLogoutRefresh, "/logout/refresh")
api.add_resource(UserService.TokenRefresh, "/token/refresh")
# Stock Service
api.add_resource(StockService.GetStock, "/stock")
api.add_resource(StockService.WatchAsset, "/watch/add")
api.add_resource(StockService.RemoveWatchedAsset, "/watch/remove")

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html.j2")

@app.route("/market")
def market():
    return render_template("market/market.html.j2")

@app.route("/login")
def login():
    return render_template("login/login.html.j2")

@app.route("/register")
def register():
    return render_template("login/register.html.j2")

@app.route("/reset-password")
def reset_password():
    return render_template("login/password-reset.html.j2")

@app.route("/account")
def account():
    return render_template("account.html.j2")

@app.route("/stock/purchase")
def stock_purchase():
    return render_template("stocks/purchase.html.j2")

@app.route("/stock/sell")
def stock_sell():
    return render_template("stocks/sell.html.j2")

if __name__ == "__main__":
    app.run(debug=True)
