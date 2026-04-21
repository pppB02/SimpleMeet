from flask import Blueprint, render_template, url_for, request, redirect, flash, session
from flask_login import logout_user, current_user
from ..web_helper import role_required
from ..user.services.customer.forms import SingUpForm, LoginForm
from .services.onboarding.businessForm import Reg_NameAndWeb, Reg_ServiceType, Reg_Location
from .services.dashboard.forms import MemberProfile
from app import db, login_manager
from ..user.services.customer.sign_up import signUpSrv
from ..user.services.customer.login import loginSrv
from .services.onboarding.finishSetup import FinishSetup
from .services.dashboard.TeamHandler import MemberAdd

business = Blueprint("business", __name__, static_folder="static", template_folder="templates", url_prefix="/business")

@business.route("/")
def index():
    return redirect(url_for("business.login"))

@business.route("/login", methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        if current_user.role == "business_admin":
            return redirect(url_for('business.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            try:
                loginSrv(email,password,remember,"business_admin")
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('business.dashboard'))
            except Exception as e:
                flash("bad password or email","danger")
                return render_template("login/login.html", form=form)
    else:
        return render_template("login/login.html", form=form)

@business.route("/logout", methods=['POST','GET'])
@role_required("business_admin","business.login")
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
        if current_user.role == "business_admin":
            return redirect(url_for('business.dashboard'))
    
    form = SingUpForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username = form.username.data
            email = form.email.data
            password = form.password.data

            try:
                signUpSrv(db,username,email,password,"business_admin")
                return redirect(url_for("business.businessName"))
            except Exception as e:
                print(e)
                return "hiba"
    else:
        return render_template("sign_up/sign_up.html", form=form)
    
@business.route("/dashboard",methods=['POST','GET'])
@role_required("business_admin","business.login")
def dashboard():
    return render_template("BDashboard/dashboard.html")


@business.route("/onboarding/business-name", methods=['POST','GET'])
@role_required("business_admin","business.login")
def businessName():
    form = Reg_NameAndWeb()
    if form.validate_on_submit():
        session['onboarding_data'] = {
            'name': form.name.data,
            'website': form.website.data
        }
        return redirect(url_for("business.businessServiceType"))
        
            
    return render_template("onboarding/business_name.html",form=form)

@business.route("/onboarding/service-type", methods=['POST','GET'])
@role_required("business_admin","business.login")
def businessServiceType():
    form = Reg_ServiceType()
    if form.validate_on_submit():
        onboarding_data = session.get('onboarding_data', {})
        onboarding_data['categories'] = form.categories.data
        session['onboarding_data'] = onboarding_data

        return redirect(url_for("business.businessLocation"))
        
            
    return render_template("onboarding/service_types.html",form=form)


@business.route("/onboarding/location", methods=['POST','GET'])
@role_required("business_admin","business.login")
def businessLocation():
    form = Reg_Location()
    if form.validate_on_submit():
        onboarding_data = session.get('onboarding_data', {})
        onboarding_data['location'] = form.location.data
        session['onboarding_data'] = onboarding_data

        print(onboarding_data)

        setup = FinishSetup(db,onboarding_data,current_user.get_id())

        try:
            setup.checkData()
            setup.SaveData()
        except Exception as e:
            print(str(e))
            return render_template("onboarding/setup_finished.html",error=str(e))


        session.pop('onboarding_data', None)
        return render_template("onboarding/setup_finished.html",error="")
        
            
    return render_template("onboarding/location.html",form=form)


@business.route("/dashboard/team", methods=['POST','GET'])
@role_required("business_admin","business.login")
def Team():
    form = MemberProfile()
    if form.validate_on_submit():
        print("Email sendingNN")
        email = form.email.data
        name = form.name.data

        print("Email sending")

        MemberAdd(email=email,name=name,business_owner_id=current_user.id)
    else:
        print("nemjo")
        print(form.errors)

    return render_template("BDashboard/team.html",form=form)