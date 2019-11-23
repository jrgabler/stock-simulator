#!/usr/bin/env python
import os
from flask import Flask, render_template, redirect, url_for
from flask import request
from flask_restful import Api
from flast_jwt_extended import JWTManager

from Api import ApiService as resources

# refactor into config.py file
VIEW_DIRECTORY = "./views"
TEMPLATE_FOLDER = os.path.abspath(VIEW_DIRECTORY + "/templates/")
STATIC_FOLDER = os.path.abspath(VIEW_DIRECTORY + "/static/")

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

app.config["JWT_SECRET_KEY"] = "jwt_secret_string"
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return False # TODO

jwt = JWTManager(app)

api = Api(app)

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')

# refactor later to appropiate place yo
# def isLoggedIn(is_log):
#     # add logic to actually check if logged in or not
#     return is_log
#
# # refactor later to appropiate place yo
# def redirectIfNotLoggedIn(is_log, redirect_url):
#     is_logged_in = isLoggedIn(is_log)
#     if is_logged_in == False:
#         return redirect(url_for(redirect_url))

@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html.j2')

@app.route("/login")
def login():
    return render_template('login/login.html.j2')

@app.route("/register")
def register():
    return render_template('login/register.html.j2')

@app.route("/reset-password")
def reset_password():
    return render_template('login/password-reset.html.j2')

@app.route("/account")
def account():
    return render_template('account.html.j2')

@app.route("/stock/purchase")
def stock_purchase():
    return render_template('stocks/purchase.html.j2')

@app.route("/stock/sell")
def stock_sell():
    return render_template('stocks/sell.html.j2')


if __name__ == "__main__":
    app.run(debug=True)
