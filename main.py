import os, sys, shutil, json, re, random, datetime, time, subprocess
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from models import *
from emailer import *
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

database = loadFromFile()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/send", methods=["POST"])
def feedbackReceived():
    global database

    # Check headers
    if 'Content-Type' not in request.headers:
        return "ERROR: Headers invalid."
    if request.headers['Content-Type'] != 'application/json':
        return "ERROR: Headers invalid."
    
    # Check body
    if 'name' not in request.json:
        return "ERROR: Body invalid."
    if 'email' not in request.json:
        return "ERROR: Body invalid."
    if 'feedback' not in request.json:
        return "ERROR: Body invalid."
    
    name = request.json['name']
    email = request.json['email']
    feedback = request.json['feedback']

    ## Generate unique ID
    id = generateAuthToken()
    while id in database["feedback"]:
        id = generateAuthToken()
    database["feedback"][id] = {
        "name": name,
        "email": email,
        "feedback": feedback
    }
    saveToFile(database)

    # Send email
    text = """
Feedback Received | Unit 731

Thanks, {}!

Thank you so much for visiting my informative website, Unit 731. 
I sincerely appreciate your feedback on your experience with the website as it helps me to make better products, content and a smoother user experience.

Your feedback form details are as shown below:

Name: {}
Email: {}
Feedback:
{}

Note that I respect your privacy and that all of your data is kept confidential. Thank you again for your time!

© Copyright 2023 Prakhar Trivedi
    """.format(name, name, email, feedback)

    Emailer.sendEmail(email, "Feedback Received | Unit 731", text, render_template("emails/feedbackReceived.html", name=name, email=email, feedback=feedback))

    return "SUCCESS: Feedback received."

## Session
@app.route("/session/<authToken>/list")
def listPage(authToken):
    global database

    ## Expire auth tokens
    database = expireAuthToken(database)
    saveToFile(database)

    if "session" in database and database["session"]["token"] == authToken:
        return render_template("list.html", authToken=authToken, feedbackData=database["feedback"])
    else:
        return redirect(url_for("errorPage", error="Invalid auth token. Access Denied."))
    
@app.route("/session/<authToken>/feedback/<id>")
def feedbackDetail(authToken, id):
    global database

    ## Expire auth tokens
    database = expireAuthToken(database)
    saveToFile(database)

    if not ("session" in database and database["session"]["token"] == authToken):
        return redirect(url_for("errorPage", error="Invalid auth token. Access Denied."))
    if id not in database["feedback"]:
        return redirect(url_for("errorPage", error="Invalid feedback ID."))
    
    return "ID: {}, Name: {}, Feedback: {}".format(id, database["feedback"][id]["name"], database["feedback"][id]["feedback"])

## API
@app.route("/api/login", methods=['POST'])
def loginUser():
    global database

    # Check headers
    if 'Content-Type' not in request.headers:
        return "ERROR: Headers invalid."
    if request.headers['Content-Type'] != 'application/json':
        return "ERROR: Headers invalid."
    if "APIKey" not in request.headers:
        return "ERROR: Headers invalid."
    if request.headers['APIKey'] != os.environ["APIKey"]:
        return "ERROR: Headers invalid."
    
    # Check body
    if 'password' not in request.json:
        return "ERROR: Body invalid."
    if request.json['password'] != os.environ["AccessPassword"]:
        return "UERROR: Incorrect password."
    
    # Generate auth token
    authToken = generateAuthToken()
    database["session"] = {
        "token": authToken,
        "lastLogin": datetime.datetime.now().strftime(datetimeFormat)
    }
    saveToFile(database)

    return "SUCCESS: Token: {}".format(authToken)

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

@app.route("/assets/indexJS")
def indexJS():
    return fileContent("supportJSFiles/index.js", passAPIKey=True)

if __name__ == '__main__':
    Emailer.checkContext()
    app.run(host='0.0.0.0', port=8000)