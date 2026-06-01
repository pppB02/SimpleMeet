from app import db, login_manager
from ..db_models import Staff, Business, Service, Appointment
from .services.ServicesHandler import addServie, addMembersToServie
from flask import Blueprint, render_template, url_for, request, redirect, flash, session, current_app
from flask_login import logout_user, current_user
from .services.dashboard.OpeningHoursService import save_opening_hours, load_opening_hours_to_form
from ..web_helper import role_required, business_required, save_photo
from ..user.services.customer.forms import SingUpForm, LoginForm
from .services.onboarding.businessForm import Reg_NameAndWeb, Reg_ServiceType, Reg_Location
from .services.dashboard.forms import (
    MemberProfile,
    ConfirmInviteForm,
    openHours,
    NewServiceForm,
    BusinessEditForm,
    AboutBusinessForm,
    UserProfileForm
)

from .services.dashboard.aboutBusiness import (
    save_about_business,
    load_about_business_to_form
)
from ..user.services.customer.sign_up import signUpSrv
from ..user.services.customer.login import loginSrv
from .services.onboarding.finishSetup import FinishSetup
from .services.dashboard.TeamHandler import MemberAdd, confirmInvite, verify_token

from .services.booking.appointment_service import (
    list_business_appointments,
    get_appointment_or_404,
    cancel_appointment_as_business,
    confirm_appointment_as_business,
    complete_appointment_as_business,
)

business = Blueprint("business", __name__, static_folder="static", template_folder="templates", url_prefix="/business")


@business.route("/")
def index():
    return redirect(url_for("business.login"))


@business.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated and current_user.role == "business_admin":
        return redirect(url_for('business.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            loginSrv(form.email.data, form.password.data, form.remember.data, "business_admin")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('business.dashboard'))
        except Exception:
            flash("bad password or email", "danger")
            return render_template("login/login.html", form=form)

    return render_template("login/login.html", form=form)


@business.route("/logout", methods=['POST', 'GET'])
@role_required("business_admin", "business.login")
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    from ..db_models import UserAccount
    return UserAccount.query.get(int(user_id))


@business.route("/sign-up", methods=['POST', 'GET'])
def signUp():
    if current_user.is_authenticated and current_user.role == "business_admin":
        return redirect(url_for('business.dashboard'))

    form = SingUpForm()
    if form.validate_on_submit():
        try:
            signUpSrv(db, form.username.data, form.email.data, form.password.data, "business_admin")
            return redirect(url_for("business.businessName"))
        except Exception as e:
            print(e)
            return "hiba"

    return render_template("sign_up/sign_up.html", form=form)


# ======================
# BUSINESS SETUP
# ======================

@business.route("/onboarding/business-name", methods=['POST', 'GET'])
@role_required("business_admin", "business.login")
def businessName():
    form = Reg_NameAndWeb()
    if form.validate_on_submit():
        session['onboarding_data'] = {
            'name': form.name.data,
            'website': form.website.data
        }
        return redirect(url_for("business.businessServiceType"))

    return render_template("onboarding/business_name.html", form=form)


@business.route("/onboarding/service-type", methods=['POST', 'GET'])
@role_required("business_admin", "business.login")
def businessServiceType():
    form = Reg_ServiceType()
    if form.validate_on_submit():
        onboarding_data = session.get('onboarding_data', {})
        onboarding_data['categories'] = form.categories.data
        session['onboarding_data'] = onboarding_data

        return redirect(url_for("business.businessLocation"))

    return render_template("onboarding/service_types.html", form=form)


@business.route("/onboarding/location", methods=['POST','GET'])
@role_required("business_admin","business.login")
def businessLocation():
    form = Reg_Location()
    if form.validate_on_submit():
        onboarding_data = session.get('onboarding_data', {})
        onboarding_data['location'] = form.location.data
        session['onboarding_data'] = onboarding_data

        setup = FinishSetup(db,onboarding_data,current_user.get_id())

        try:
            setup.checkData()
            setup.SaveData()
        except Exception as e:
            print(str(e))
            return render_template("onboarding/setup_finished.html",error=str(e))

        session.pop('onboarding_data', None)
        return redirect(url_for("business.aboutBusiness"))

    return render_template("onboarding/location.html",form=form)


# ======================
# CONFIRM TEAM LINK
# ======================

@business.route("/confirm-invite/<token>", methods=['POST', 'GET'])
def confirmInviteSite(token):
    if not current_user.is_authenticated:
        return redirect(url_for("user.login", next=request.url))

    if current_user.role != "customer":
        return redirect(url_for("user.login"))

    datas = verify_token(token)
    if not datas:
        return "Invalid or expired token"

    form = ConfirmInviteForm()
    if form.validate_on_submit():
        if form.agreeTerms.data:
            try:
                confirmInvite(current_user.email, datas)
                return redirect(url_for("user.dashboard"))
            except Exception as e:
                print(e)
                return render_template("confirm_invite/confirm_invite.html", form=form, error=str(e))

    return render_template("confirm_invite/confirm_invite.html", form=form)


# ======================
# DASHBOARD
# ======================

@business.route("/dashboard", methods=['POST', 'GET'])
@business_required()
def dashboard():
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()
    appointments_count = Appointment.query.filter_by(business_id=business_obj.id).count()
    staff_count = Staff.query.filter_by(business_id=business_obj.id).count()
    service_count = Service.query.filter_by(business_id=business_obj.id).count()

    return render_template(
        "BDashboard/dashboard.html",
        business=business_obj,
        appointments_count=appointments_count,
        staff_count=staff_count,
        service_count=service_count
    )


@business.route("/dashboard/team-members", methods=['POST', 'GET'])
@business_required()
def team():
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()
    membersTable = Staff.query.filter_by(business_id=business_obj.id).all()

    return render_template("BDashboard/team/team.html", membersTable=membersTable, business=business_obj)


@business.route("/dashboard/team-add-member", methods=['POST', 'GET'])
@business_required()
def teamMembers():
    form = MemberProfile()
    filename = None

    if form.validate_on_submit():
        photo = form.photo.data
        email = form.email.data
        name = form.name.data

        filename = save_photo(photo)
        if not filename:
            filename = "default.jpg"

        MemberAdd(email=email, name=name, business_owner_id=current_user.id, pfp=filename)
        return redirect(url_for("business.team"))

    return render_template("BDashboard/team/team_add_member.html", form=form, filename=filename)


@business.route("/dashboard/hours", methods=['POST', 'GET'])
@business_required()
def hours():
    form = openHours()
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()

    if request.method == "GET":
        load_opening_hours_to_form(business_obj.id, form)

    if form.validate_on_submit():
        save_opening_hours(business_obj.id, form)
        flash("Nyitvatartás mentve", "success")
        return redirect(url_for("business.hours"))

    days = ["mon", "tue", "wen", "thu", "fri", "sat", "sun"]
    return render_template("BDashboard/hours/hours.html", form=form, days=days, business=business_obj)


@business.route("/dashboard/catalog", methods=['POST', 'GET'])
@business_required()
def catalog():
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()
    services = Service.query.filter_by(business_id=business_obj.id).order_by(Service.name.asc()).all()

    return render_template(
        "BDashboard/service/catalog.html",
        business=business_obj,
        services=services
    )


@business.route("/dashboard/new-service", methods=['POST', 'GET'])
@business_required()
def newService():
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()
    teamMembersData = Staff.query.filter_by(business_id=business_obj.id).all()
    form = NewServiceForm(teamMembersData=teamMembersData)

    if form.validate_on_submit():
        datas = {
            "business_id": business_obj.id,
            "name": form.name.data,
            "serviceType": form.serviceType.data,
            "description": form.description.data,
            "duration": int(form.duration.data),
            "price_type": form.priceType.data,
            "price": int(form.price.data),
        }

        service_id = addServie(datas)

        if form.teamMembers.data and str(form.teamMembers.data) != "0":
            selected_staff = Staff.query.filter_by(
                id=int(form.teamMembers.data),
                business_id=business_obj.id
            ).first()

            if selected_staff:
                addMembersToServie([selected_staff], service_id)

        flash("Szolgáltatás mentve", "success")
        return redirect(url_for("business.catalog"))

    return render_template("BDashboard/service/newService.html", form=form)

@business.route("/dashboard/about-business", methods=['POST', 'GET'])
@business_required()
def aboutBusiness():
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()
    form = AboutBusinessForm()
    if request.method == "GET":
        load_about_business_to_form(business_obj, form)

    if form.validate_on_submit():
        try:
            raw_tags = request.form.get('selected_tags_submit', '')
            save_about_business(business_obj, form, raw_tags)
            flash("Az üzlet bemutatkozó oldala mentve.", "success")
            return redirect(url_for("business.aboutBusiness"))
        except Exception as e:
            flash(str(e), "danger")

    return render_template(
        "BDashboard/about/about_business.html",
        form=form,
        business=business_obj,
    )

@business.route("/dashboard/edit-business", methods=["GET", "POST"])
@business_required()
def edit_business():
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()
    form = BusinessEditForm()

    if request.method == "GET":
        form.name.data = business_obj.name
        form.location.data = business_obj.location
        form.website.data = business_obj.website

    if form.validate_on_submit():
        business_obj.name = form.name.data
        business_obj.location = form.location.data
        business_obj.website = form.website.data

        db.session.commit()
        flash("Az üzlet adatai mentve.", "success")
        return redirect(url_for("business.edit_business"))

    return render_template(
        "BDashboard/settings/edit_business.html",
        form=form,
        business=business_obj
    )

# ======================
# APPOINTMENTS (BUSINESS ADMIN)
# ======================

@business.route("/dashboard/appointments", methods=["GET"])
@business_required()
def appointments():
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()
    appointments = list_business_appointments(business_obj.id)

    return render_template(
        "BDashboard/appointments/calendar.html",
        business=business_obj,
        appointments=appointments
    )


@business.route("/dashboard/appointments/<int:appointment_id>", methods=["GET"])
@business_required()
def appointment_detail(appointment_id):
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()
    appointment = get_appointment_or_404(appointment_id)

    if appointment.business_id != business_obj.id:
        return "Forbidden", 403

    return render_template(
        "BDashboard/appointments/detail.html",
        business=business_obj,
        appointment=appointment
    )


@business.route("/dashboard/appointments/<int:appointment_id>/confirm", methods=["POST"])
@business_required()
def appointment_confirm(appointment_id):
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()
    try:
        appointment = confirm_appointment_as_business(appointment_id, business_obj.id)
        flash("Foglalás visszaigazolva.", "success")
        return redirect(url_for("business.appointment_detail", appointment_id=appointment.id))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("business.appointment_detail", appointment_id=appointment_id))


@business.route("/dashboard/appointments/<int:appointment_id>/complete", methods=["POST"])
@business_required()
def appointment_complete(appointment_id):
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()
    try:
        appointment = complete_appointment_as_business(appointment_id, business_obj.id)
        flash("Foglalás készre jelölve.", "success")
        return redirect(url_for("business.appointment_detail", appointment_id=appointment.id))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("business.appointment_detail", appointment_id=appointment_id))


@business.route("/dashboard/appointments/<int:appointment_id>/cancel", methods=["POST"])
@business_required()
def appointment_cancel(appointment_id):
    business_obj = Business.query.filter_by(admin_user_id=current_user.id).first()
    try:
        appointment = cancel_appointment_as_business(appointment_id, business_obj.id)
        flash("Foglalás lemondva.", "success")
        return redirect(url_for("business.appointment_detail", appointment_id=appointment.id))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("business.appointment_detail", appointment_id=appointment_id))