from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import logout_user, current_user
from ..web_helper import role_required
from .services.customer.forms import SingUpForm, LoginForm
from app import db, login_manager
from .services.customer.sign_up import signUpSrv
from .services.customer.login import loginSrv

user = Blueprint("user", __name__, static_folder="static", template_folder="templates", url_prefix="/user")

@user.route("/login", methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        if current_user.role == "customer":
            return redirect(url_for('user.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            try:
                loginSrv(email,password,remember,"customer")
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('user.dashboard'))
            except Exception as e:
                flash("bad password or email","danger")
                return render_template("customer/login/login.html", form=form)
    else:
        return render_template("customer/login/login.html", form=form)

@user.route("/logout", methods=['POST','GET'])
@role_required("customer","user.login")
def logout():
    logout_user()
    return redirect("/")

@login_manager.user_loader
def load_user(user_id):
    from ..db_models import UserAccount
    return UserAccount.query.get(int(user_id))

@user.route("/sign-up", methods=['POST','GET'])
def signUp():
    if current_user.is_authenticated:
        if current_user.role == "customer":
            return redirect(url_for('user.dashboard'))
    
    form = SingUpForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username = form.username.data
            email = form.email.data
            password = form.password.data

            try:
                signUpSrv(db,username,email,password,"customer")
                return redirect(url_for("user.dashboard"))
            except Exception as e:
                print(e)
                return "hiba"
    else:
        return render_template("customer/sign_up/sign_up.html", form=form)
    
@user.route("/dashboard")
@role_required("customer","user.login")
def dashboard():
    return render_template("dashboard/dashboard.html")