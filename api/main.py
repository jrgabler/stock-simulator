#!/usr/bin/env python

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return "System active"

app.run(host="0.0.0.0")
