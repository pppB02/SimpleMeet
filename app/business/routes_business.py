from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import logout_user, current_user, login_required
from ..user.services.customer.forms import SingUpForm, LoginForm
from .services.onboarding.businessForm import NameAndWebsite
from app import db, login_manager
from ..user.services.customer.sign_up import signUpSrv
from ..user.services.customer.login import loginSrv

business = Blueprint("business", __name__, static_folder="static", template_folder="templates", url_prefix="/business")

@business.route("/")
def index():
    return redirect(url_for("business.login"))

@business.route("/login", methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('business.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            try:
                loginSrv(email,password,remember)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('business.dashboard'))
            except Exception as e:
                flash("bad password or email","danger")
                return render_template("login/login.html", form=form)
    else:
        return render_template("login/login.html", form=form)

@business.route("/logout", methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    return redirect("/")

@login_manager.user_loader
def load_user(user_id):
    from ..db_models import UserAccount
    return UserAccount.query.get(int(user_id))

@business.route("/sign-up", methods=['POST','GET'])
def signUp():
    if current_user.is_authenticated:
        return redirect(url_for('business.dashboard'))
    
    form = SingUpForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username = form.username.data
            email = form.email.data
            password = form.password.data

            try:
                signUpSrv(db,username,email,password,"business_admin")
                return redirect(url_for("business.onboarding"))
            except Exception as e:
                print(e)
                return "hiba"
    else:
        return render_template("sign_up/sign_up.html", form=form)
    
@business.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html")

@business.route("/onboarding/business_name")
@login_required
def onboarding():
    form = NameAndWebsite()
    if form.validate_on_submit():
        if request.method == "POST":
            business_name = form.business_name.data
            website = form.website.data

            try:
                #signUpSrv(db,username,email,password,"business_admin")
                return redirect(url_for("business.onboarding"))
            except Exception as e:
                print(e)
                return "hiba"
    return render_template("onboarding/business_name.html",form=form)
