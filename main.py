import os, sys, shutil, json, re, random, datetime, time, subprocess
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from models import *
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

database = loadFromFile()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/session/<authToken>/list")
def listPage(authToken):
    global database

    if "session" in database and database["session"]["token"] == authToken:
        return "Access Granted"
    else:
        return redirect(url_for("errorPage", error="Invalid auth token. Access Denied."))

## Misc
@app.route("/security/error")
def errorPage():
    if 'error' not in request.args:
        return render_template("error.html", error=None)
    else:
        return render_template("error.html", error=request.args['error'])

## Assets
@app.route("/assets/copyright")
def copyright():
    return fileContent("copyright.js")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)