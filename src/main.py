#!/usr/bin/env python

import os
from flask import Flask, render_template
from flask import request

# refactor into config.py file
VIEW_DIRECTORY = "./views"
TEMPLATE_FOLDER = os.path.abspath(VIEW_DIRECTORY + "/templates/")
STATIC_FOLDER = os.path.abspath(VIEW_DIRECTORY + "/static/")

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

@app.route("/")
def index():
    return render_template('index.html.j2')

@app.route("/login")
def login():
    return render_template('login/login.html.j2')

@app.route("/register")
def register():
    return render_template('login/register.html.j2')

@app.route("/account")
def account():
    return render_template('account.html.j2')

if __name__ == "__main__":
    app.run(debug=True)
