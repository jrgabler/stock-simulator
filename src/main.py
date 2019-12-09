#!/usr/bin/env python
import os, requests
from flask import Flask, render_template, redirect, url_for
from flask import request
from flask_restful import Api
from flask_jwt_extended import JWTManager

from Api import UserService, StockService
from Controllers import UserController

# refactor into config.py file
VIEW_DIRECTORY = "./views"
TEMPLATE_FOLDER = os.path.abspath(VIEW_DIRECTORY + "/templates/")
STATIC_FOLDER = os.path.abspath(VIEW_DIRECTORY + "/static/")
LOCAL_URL = 'https://localhost:5000'
HEADERS = {"Authorization": '', "Accept": "application/json"}


app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

app.config["JWT_SECRET_KEY"] = "jwt_secret_string"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

blacklist = set()
jwt = JWTManager(app)
api = Api(app)

# called every time client tries to access a secure endpoint
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return UserController.tokenIsBlacklisted(jti)


# User Service
api.add_resource(UserService.UserRegistration, "/registration")
api.add_resource(UserService.UserLogin, "/login/submit")
api.add_resource(UserService.UserLogoutAccess, "/logout/access")
api.add_resource(UserService.UserLogoutRefresh, "/logout/refresh")
api.add_resource(UserService.TokenRefresh, "/token/refresh")
# Stock Service
api.add_resource(StockService.GetStock, "/stock")
api.add_resource(StockService.WatchAsset, "/watch/add")
api.add_resource(StockService.RemoveWatchedAsset, "/watch/remove")


#  isLogged in to be removed and replaced for Token Access check
def isLoggedIn(template, isLoggedIn):
    if isLoggedIn:
        return render_template(template)

    return redirect(url_for('login'))

@app.route("/")
@app.route("/home")
def index():
    return isLoggedIn("index.html.j2", True)

@app.route("/market")
def market():
    return isLoggedIn("market/market.html.j2", True)

@app.route("/login")
def login():
    return render_template("login/login.html.j2") #, data=r.json())

@app.route('/login', methods=['POST'])
def login_submission():
    r = requests.post(LOCAL_URL + '/login/access',
        params={
            'username': request.form['username'],
            'password': request.form['password']
    })

    return '<html><p>yo:' + r.json + '</p><html>';


    # if request.method == 'POST':
    #     r = requests.post('/login/access', auth=('user', 'pass')

    # r = requests.post('/login/access', auth=('user', 'pass')
    # r.json();


@app.route("/register")
def register():
    # if
    return isLoggedIn("login/register.html.j2", True)

@app.route("/reset-password")
def reset_password():
    return isLoggedIn("login/password-reset.html.j2", True)

@app.route("/account")
def account():
    return isLoggedIn("account.html.j2", True)

@app.route("/stock/purchase")
def stock_purchase():
    return isLoggedIn("stocks/purchase.html.j2", True)

@app.route("/stock/sell")
def stock_sell():
    return isLoggedIn("stocks/sell.html.j2", True)

@app.route("/watchlist/manage")
def manage_watchlist():
    # if request.method == "POST":
    #     # flash('Login requested for user {}, remember_me={}'.format(
    #     #     form.username.data, form.remember_me.data))
    #     return redirect('/index')
    return isLoggedIn("watchlist/manage.html.j2", True)

@app.route("/watchlist/manage/add")
def add_stock_watchlist():
    return isLoggedIn("stocks/purchase.html.j2", True)

@app.route("/watchlist/manage/remove")
def remove_stock_watchlist():
    return isLoggedIn("stocks/purchase.html.j2", True)

if __name__ == "__main__":
    app.run(host='0.0.0.0')    # Dockerized
    # app.run(debug=True)    # Debug
