######################################################################################################
# ________           .__   .__                        _____                    __              __    #
# \_____  \    ____  |  |  |__|  ____    ____        /     \  _____   _______ |  | __  ____  _/  |_  #
#  /   |   \  /    \ |  |  |  | /    \ _/ __ \      /  \ /  \ \__  \  \_  __ \|  |/ /_/ __ \ \   __\ #
# /    |    \|   |  \|  |__|  ||   |  \\  ___/     /    Y    \ / __ \_ |  | \/|    < \  ___/  |  |   #
# \_______  /|___|  /|____/|__||___|  / \___  >    \____|__  /(____  / |__|   |__|_ \ \___  > |__|   #
#         \/      \/                \/      \/             \/      \/              \/     \/         #
#                                                                                                    #
#                             github: prizrak3742, Solochuk, xztick                                  #
######################################################################################################

############ IMPORTS ############

import os
import sys
from flask import Flask, make_response, render_template, request, g, flash, abort, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import connection_db
from db_config import db_name, user, password
from function_db import DataBase
from UserLogin import UserLogin

############ CONFIGURATION ############

DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
dbase = None
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@localhost/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "You need sign in to site for read this page!"
login_manager.login_message_category = "error"

############ ERRORS & REQUESTS ############

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id)

@app.before_request
def before_request():
    global db
    db = DataBase()

############ ROUTERS | USER ############

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def index_product():
    return render_template("index.html")

@app.route("/products/<type>")
def products(type):
    product_list = db.get_ad_by_product(type)
    product_type = db.get_type_by_id(type)[0]["product_type"]

    return render_template("products.html", product_list=product_list, prod_type=product_type)

@app.route("/product_<id>")
def product(id):
    product_list = db.get_product_by_id(id)[0]
    product_type = db.get_type_by_id(product_list["product_type_id"])[0]["product_type"]
    return render_template("product.html", title=product_list["title"], price=product_list["price"], description=product_list["description"],
                           user_id=product_list["user_id"], photo=product_list["photo"], catycogry=product_type)

@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")
        number = int(request.form.get("phone"))

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for("registration"))

        hashed_password = generate_password_hash(password)
        try:
            res = db.create_account(name, email, hashed_password, number=number)
            print(res)
        except Exception as e:
            print(e)


    return render_template("registration.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        user = db.get_user_by_email(request.form['email'])
        if user and check_password_hash(user[0]['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for(f"profile"))

        flash("The password or login not correct", "error")

    return render_template("login.html")


@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    name = current_user.getName()
    email = current_user.getEmail()
    phone = current_user.getPhone()
    return render_template("profile.html", name=name, email=email, phone=phone)

@app.route("/add_ad", methods=["POST", "GET"])
def add_ad():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        category = request.form.get("category")
        price = request.form.get("price")
        image = request.files.get("image")

        if image:
            image_path = f'static/uploads/{image.filename}'
            image.save(image_path)

        result = db.add_post(title, description, category, price, current_user.get_id(), image_path)

        if result[1] == "success":
            flash("Ad successfully added!", "success")
            return redirect(url_for("index"))
        else:
            flash(result[0], "error")

    return render_template("add_ad.html")



############ ROUTERS | ADMIN ############

############ RUN | RUN ############

if __name__ == "__main__":
    app.run(debug=DEBUG)
