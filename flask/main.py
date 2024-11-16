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
from flask_mail import Mail, Message
import random
from PIL import Image
from io import BytesIO
############ CONFIGURATION ############

DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
dbase = None
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@localhost/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465 
app.config['MAIL_USERNAME'] = 'goustg62@gmail.com'
app.config['MAIL_PASSWORD'] = 'zlxy gfmc qjke cknb'
app.config['MAIL_DEFAULT_SENDER'] = 'goustg62@gmail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
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

@app.route("/product_<id>", methods=["GET", "POST"]) 
@login_required
def product(id):
    product_list = db.get_product_by_id(id)[0]
    user_id = product_list["user_id"]
    user = db.get_user_by_id(user_id)[0]
    product_type = db.get_type_by_id(product_list["product_type_id"])[0]["product_type"]

    id = product_list["id"]

    image = Image.open(BytesIO(product_list["photo"]))
    directory = f'static/img/{id}.jpg'
    if not os.path.isfile(directory): 
        image.save(directory)
    
    comments = db.get_comments(id)
    
    if request.method == "POST":
        comment = request.form.get("comment")
        if comment:
            user_id = current_user.get_id()
            db.add_comment(comment, id, user_id) 
            return redirect(url_for('product', id=id))
    
    return render_template("product.html", 
                           title=product_list["title"], 
                           price=product_list["price"], 
                           description=product_list["description"], 
                           user_id=product_list["user_id"], 
                           photo=directory, 
                           catycogry=product_type, 
                           comments=comments,
                           name=user["name"],
                           phone=user["number"])


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
        return redirect(url_for('profile_'))

    if request.method == "POST":
        user = db.get_user_by_email(request.form['email'])
        if user and check_password_hash(user[0]['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or redirect(url_for("profile_")))

        flash("The password or login not correct", "error")

    return render_template("login.html")

@app.route("/profile/<id>", methods=["POST", "GET"])
@login_required
def profile(id):
    name = current_user.getName()
    email = current_user.getEmail()
    phone = current_user.getPhone()
    auth = bool(db.get_auth(email)[0]['auth'])
    return render_template("profile.html", name=name, email=email, phone=phone, auth=auth)

@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile_():
    id = current_user.get_id()
    return redirect(url_for("profile", id=id))

@app.route("/confirm_email", methods=["POST", "GET"])
@login_required
def confirm_email():

    try:
        email = current_user.getEmail()
        auth = bool(db.get_auth(email)[0]['auth'])
        code = random.randint(111111111, 999999999)
        list = [code]
        if not auth:
            msg = Message('Event reminder', recipients=[email])
            msg.body = 'Code | Online Market'
            msg.html = str(code)
            mail.send(msg)
            if request.method == "POST":
                confirmationCode = request.form.get("confirmationCode")
                print("confirmationCode:", confirmationCode)
                print("code: ", code)
                if str(list[0]) == str(code):
                    db.accept_auth(email)
                    return redirect(url_for("profile_"))
        else:
            return redirect(url_for("profile_"))
    
    except Exception as e:
        print(e)

    return render_template("confirm_email.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Success! You log out from account!", "success")
    return redirect(url_for('login'))

@app.route("/add_ad", methods=["POST", "GET"])
@login_required
def add_ad():
    if request.method == "POST":
        user_id = current_user.get_id()
        title = request.form.get('adTitle') # з форм, яка має id 'adTitle'
        description = request.form.get('adDescription')
        category = db.get_id_by_type(request.form.get('adCategory'))[0]["id"]
        print(category)
        price = request.form.get('adPrice')
        image = request.files.get('adImage')
        image_data = image.read() if image else None
        db.add_ad(user_id=user_id, title=title, description=description, category=category, price=price, image=image_data)
    
    return render_template("add_ad.html")



############ RUN | RUN ############

if __name__ == "__main__":
    app.run(debug=DEBUG)