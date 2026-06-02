from collections import defaultdict
from datetime import datetime
from ..web_helper import time_format
from flask import Blueprint, render_template, url_for, send_from_directory, current_app, jsonify, request
from flask_login import current_user
from .services.constans import FURTHER_INFO_CHOICES, SERVICE_TYPES
from ..db_models import Business, Staff, UserAccount, Service, Appointment, OpeningHour
from app import db
from ..business.services.booking.availability import generate_slots
from ..business.services.booking.booking_service import create_appointment

index = Blueprint("index", __name__, static_folder="static", template_folder="templates", static_url_path="/index/static")


@index.route("/get_file/<filename>")
def get_file(filename):
    return send_from_directory(current_app.config["UPLOADED_PHOTOS_DEST"], filename)


@index.route("/")
def home():
    featured_businesses = Business.query.filter(
        Business.about_description.isnot(None)
    ).order_by(Business.id.desc()).all()

    return render_template(
        "index.html",
        featured_businesses=featured_businesses
    )


@index.route("/data-protection")
def dataProtection():
    return render_template("adatvedelem.html")

@index.route("/terms-of-service")
def termsOfService():
    return render_template("adatvedelem.html")

@index.route("/book/<slug>")
def business_book(slug):
    public_id = slug.rsplit("-", 1)[-1]
    business = Business.query.filter_by(public_id=public_id).first_or_404()

    staffs = Staff.query.filter_by(business_id=business.id).all()
    staffDatas = []
    for staff in staffs:
        staffUser = UserAccount.query.filter_by(id=staff.user_id).first()
        staffDatas.append({
            "id": staff.id,
            "name": staffUser.username if staffUser else "Ismeretlen",
            "pfp_name": staff.pfp_name,
            "services": [service.id for service in staff.services],
        })

    services = Service.query.filter_by(business_id=business.id, is_active=True).all()
    serviceDatas = defaultdict(list)
    for service in services:
        serviceDatas[service.serviceType].append(service)

    opening_hours = OpeningHour.query.filter_by(business_id=business.id).all()
    preselected_service = request.args.get("service", type=int)

    services_payload = [
        {
            "id": service.id,
            "name": service.name,
            "type": service.serviceType,
            "duration": service.duration,
            "price": str(service.price),
            "description": service.description or "",
        }
        for service in services
    ]

    return render_template(
        "temp_for_services/test.html",
        business=business,
        staffs=staffDatas,
        serviceDatas=dict(serviceDatas),
        services=services,
        services_payload=services_payload,
        opening_hours=opening_hours,
        time_format=time_format,
        preselected_service=preselected_service,
        SERVICE_TYPES = SERVICE_TYPES
    )


@index.route("/a/<slug>")
def business_site(slug):
    public_id = slug.rsplit("-", 1)[-1]
    business = Business.query.filter_by(public_id=public_id).first_or_404()

    staffs = Staff.query.filter_by(business_id=business.id).all()
    staffDatas = []
    for staff in staffs:
        staffUser = UserAccount.query.filter_by(id=staff.user_id).first()
        staffDatas.append({
            "id": staff.id,
            "name": staffUser.username if staffUser else "Ismeretlen",
            "pfp_name": staff.pfp_name,
            "services": [service.id for service in staff.services],
        })

    services = Service.query.filter_by(business_id=business.id, is_active=True).all()
    serviceDatas = defaultdict(list)
    for service in services:
        serviceDatas[service.serviceType].append(service)

    opening_hours = OpeningHour.query.filter_by(business_id=business.id).all()
    preselected_service = request.args.get("service", type=int)

    services_payload = [
        {
            "id": service.id,
            "name": service.name,
            "type": service.serviceType,
            "duration": service.duration,
            "price": str(service.price),
            "description": service.description or "",
        }
        for service in services
    ]
    return render_template(
        "temp_for_services/szolgaltatas_minta.html",
        business=business,
        staffs=staffDatas,
        serviceDatas=dict(serviceDatas),
        services=services,
        services_payload=services_payload,
        opening_hours=opening_hours,
        time_format=time_format,
        preselected_service=preselected_service,
        SERVICE_TYPES = SERVICE_TYPES,
        infos = [
        FURTHER_INFO_CHOICES[i]
        for i in business.further_info
    ]
    )

@index.route("/api/availability")
def availability():
    business_id = request.args.get("business_id", type=int)
    staff_id = request.args.get("staff_id", type=int)
    service_id = request.args.get("service_id", type=int)
    date_str = request.args.get("date")

    if not all([business_id, staff_id, service_id, date_str]):
        return jsonify({"slots": []}), 400

    date = datetime.fromisoformat(date_str).date()

    service = Service.query.get_or_404(service_id)
    staff = Staff.query.get_or_404(staff_id)

    if staff.business_id != business_id or service.business_id != business_id:
        return jsonify({"slots": []}), 400

    if service not in staff.services:
        return jsonify({"slots": []}), 400

    opening_hour = OpeningHour.query.filter_by(
        business_id=business_id,
        day_of_week=date.weekday(),
    ).first()

    if not opening_hour or opening_hour.is_closed or not opening_hour.open_time or not opening_hour.close_time:
        return jsonify({"slots": []})

    appointments = Appointment.query.filter(
        Appointment.staff_id == staff_id,
        Appointment.status.in_(["pending", "confirmed"]),
        db.func.date(Appointment.start_at) == date,
    ).all()

    slots = generate_slots(
        date=date,
        open_time=opening_hour.open_time,
        close_time=opening_hour.close_time,
        duration_minutes=service.duration,
        existing_appointments=appointments,
    )

    return jsonify(
        {
            "slots": [
                {
                    "start_at": slot["start_at"].isoformat(),
                    "end_at": slot["end_at"].isoformat(),
                }
                for slot in slots
            ]
        }
    )


@index.route("/api/book", methods=["POST"])
def book():
    if not current_user.is_authenticated:
        return jsonify({"error": "login_required"}), 401

    if current_user.role != "customer":
        return jsonify({"error": "only_customer_can_book"}), 403

    data = request.get_json(force=True)

    try:
        appointment = create_appointment(
            user_id=current_user.id,
            business_id=int(data["business_id"]),
            service_id=int(data["service_id"]),
            staff_id=int(data["staff_id"]),
            start_at=datetime.fromisoformat(data["start_at"]),
            notes=data.get("notes"),
        )

        return jsonify(
            {
                "success": True,
                "appointment_id": appointment.id,
                "start_at": appointment.start_at.isoformat(),
                "end_at": appointment.end_at.isoformat(),
            }
        ), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400