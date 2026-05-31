from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import logout_user, current_user

from ..web_helper import role_required, staff_profile_required
from .services.customer.forms import SingUpForm, LoginForm
from app import db, login_manager
from .services.customer.sign_up import signUpSrv
from .services.customer.login import loginSrv

from ..business.services.booking.appointment_service import (
    list_customer_appointments,
    list_staff_appointments,
    get_appointment_or_404,
    cancel_appointment_as_customer,
    cancel_appointment_as_staff,
    confirm_appointment_as_staff,
    complete_appointment_as_staff,
)

user = Blueprint("user", __name__, static_folder="static", template_folder="templates", url_prefix="/user")


@user.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated and current_user.role == "customer":
        return redirect(url_for('user.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            loginSrv(form.email.data, form.password.data, form.remember.data, "customer")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user.dashboard'))
        except Exception:
            flash("bad password or email", "danger")
            return render_template("customer/login/login.html", form=form)

    return render_template("customer/login/login.html", form=form)


@user.route("/logout", methods=['POST', 'GET'])
@role_required("customer", "user.login")
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    from ..db_models import UserAccount
    return UserAccount.query.get(int(user_id))


@user.route("/sign-up", methods=['POST', 'GET'])
def signUp():
    if current_user.is_authenticated and current_user.role == "customer":
        return redirect(url_for('user.dashboard'))

    form = SingUpForm()
    if form.validate_on_submit():
        try:
            signUpSrv(db, form.username.data, form.email.data, form.password.data, "customer")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user.dashboard'))
        except Exception as e:
            print(e)
            return "hiba"

    return render_template("customer/sign_up/sign_up.html", form=form)


@user.route("/dashboard")
@role_required("customer", "user.login")
def dashboard():
    if getattr(current_user, "staff_profile", None):
        return redirect(url_for("user.staff_dashboard"))

    appointments = list_customer_appointments(current_user.id)
    return render_template(
        "dashboard/dashboard.html",
        appointments=appointments,
        is_staff=False
    )


# ======================
# CUSTOMER BOOKINGS
# ======================

@user.route("/dashboard/bookings")
@role_required("customer", "user.login")
def customer_bookings():
    if getattr(current_user, "staff_profile", None):
        return redirect(url_for("user.staff_dashboard"))

    appointments = list_customer_appointments(current_user.id)
    return render_template(
        "dashboard/bookings.html",
        appointments=appointments,
        is_staff=False
    )


@user.route("/dashboard/bookings/<int:appointment_id>")
@role_required("customer", "user.login")
def customer_booking_detail(appointment_id):
    appointment = get_appointment_or_404(appointment_id)

    if appointment.user_id != current_user.id:
        return "Forbidden", 403

    return render_template(
        "dashboard/booking_detail.html",
        appointment=appointment,
        is_staff=False
    )


@user.route("/dashboard/bookings/<int:appointment_id>/cancel", methods=["POST"])
@role_required("customer", "user.login")
def customer_booking_cancel(appointment_id):
    try:
        appointment = cancel_appointment_as_customer(appointment_id, current_user.id)
        flash("A foglalás sikeresen lemondva.", "success")
        return redirect(url_for("user.customer_booking_detail", appointment_id=appointment.id))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("user.customer_booking_detail", appointment_id=appointment_id))


# ======================
# STAFF DASHBOARD
# ======================

@user.route("/staff/dashboard")
@staff_profile_required("user.dashboard")
def staff_dashboard():
    staff = current_user.staff_profile
    appointments = list_staff_appointments(staff.id)

    return render_template(
        "dashboard/dashboard.html",
        appointments=appointments,
        is_staff=True,
        staff=staff
    )


@user.route("/staff/dashboard/bookings")
@staff_profile_required("user.dashboard")
def staff_bookings():
    staff = current_user.staff_profile
    appointments = list_staff_appointments(staff.id)

    return render_template(
        "dashboard/bookings.html",
        appointments=appointments,
        is_staff=True,
        staff=staff
    )


@user.route("/staff/dashboard/bookings/<int:appointment_id>")
@staff_profile_required("user.dashboard")
def staff_booking_detail(appointment_id):
    staff = current_user.staff_profile
    appointment = get_appointment_or_404(appointment_id)

    if appointment.staff_id != staff.id:
        return "Forbidden", 403

    return render_template(
        "dashboard/booking_detail.html",
        appointment=appointment,
        is_staff=True
    )


@user.route("/staff/dashboard/bookings/<int:appointment_id>/confirm", methods=["POST"])
@staff_profile_required("user.dashboard")
def staff_booking_confirm(appointment_id):
    staff = current_user.staff_profile
    try:
        appointment = confirm_appointment_as_staff(appointment_id, staff.id)
        flash("A foglalás visszaigazolva.", "success")
        return redirect(url_for("user.staff_booking_detail", appointment_id=appointment.id))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("user.staff_booking_detail", appointment_id=appointment_id))


@user.route("/staff/dashboard/bookings/<int:appointment_id>/complete", methods=["POST"])
@staff_profile_required("user.dashboard")
def staff_booking_complete(appointment_id):
    staff = current_user.staff_profile
    try:
        appointment = complete_appointment_as_staff(appointment_id, staff.id)
        flash("A foglalás készre jelölve.", "success")
        return redirect(url_for("user.staff_booking_detail", appointment_id=appointment.id))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("user.staff_booking_detail", appointment_id=appointment_id))


@user.route("/staff/dashboard/bookings/<int:appointment_id>/cancel", methods=["POST"])
@staff_profile_required("user.dashboard")
def staff_booking_cancel(appointment_id):
    staff = current_user.staff_profile
    try:
        appointment = cancel_appointment_as_staff(appointment_id, staff.id)
        flash("A foglalás lemondva.", "success")
        return redirect(url_for("user.staff_booking_detail", appointment_id=appointment.id))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("user.staff_booking_detail", appointment_id=appointment_id))