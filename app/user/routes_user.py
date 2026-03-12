from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import logout_user, login_required
from app import db, login_manager
from .services.customer.sign_up import signUpSrv
from .services.customer.login import loginSrv

user = Blueprint("user", __name__, static_folder="static", template_folder="templates", url_prefix="/user")

@user.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password').encode("utf-8")

        page = loginSrv(db,username,email,password)
        return page
    else:
        return render_template("customer/login/login.html", error="")

@user.route("/logout", methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    return redirect("/")

@login_manager.user_loader
def load_user(user_id):
    from ..db_models import UserAccount
    return UserAccount.query.get(int(user_id))

@user.route("/sign-up", methods=['POST','GET'])
def signUp():
    if request.method == "POST":
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            page = signUpSrv(db,username,email,password)
            return page
        except:
            return "There was an issue adding your task"
    else:
        return render_template("customer/sign_up/sign_up.html")
    
@user.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html")