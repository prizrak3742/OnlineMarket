######################################################################################################
# ________           .__   .__                        _____                    __              __    #
# \_____  \    ____  |  |  |__|  ____    ____        /     \  _____   _______ |  | __  ____  _/  |_  #
#  /   |   \  /    \ |  |  |  | /    \ _/ __ \      /  \ /  \ \__  \  \_  __ \|  |/ /_/ __ \ \   __\ #
# /    |    \|   |  \|  |__|  ||   |  \\  ___/     /    Y    \ / __ \_ |  | \/|    < \  ___/  |  |   #
# \_______  /|___|  /|____/|__||___|  / \___  >    \____|__  /(____  / |__|   |__|_ \ \___  > |__|   #
#         \/      \/                \/      \/             \/      \/              \/     \/         #
#                                                                                                    #
#                                    github: prizrak3742, Solochuk                                   #
######################################################################################################

############ IMPORTS ############

import os
import sys
from flask import Flask, make_response, render_template, request, g, flash, abort, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import connection_db

############ CONFIGURATION ############

DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
dbase = None
app = Flask(__name__)
app.config.from_object(__name__)
#login_manager = LoginManager(app)
#login_manager.login_view = 'login'
#login_manager.login_message = "You need sign in to site for read this page!"
#login_manager.login_message_category = "error"

############ ERRORS & REQUESTS ############

@app.before_request
def before_request():
    global db
    db = connection_db()

############ ROUTERS | USER ############

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    return render_template("registration.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/profile", methods=["POST", "GET"])
def profile():
    return render_template("profile.html")

@app.route("/add_ad", methods=["POST", "GET"])
def add_ad():
    return render_template("add_ad.html")

############ ROUTERS | ADMIN ############

############ RUN | RUN ############

if __name__ == "__main__":
    app.run(debug=True)