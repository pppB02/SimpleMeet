from datetime import datetime

from flask import abort
from app import db
from ....db_models import Appointment


def list_customer_appointments(user_id: int):
    return (
        Appointment.query
        .filter_by(user_id=user_id)
        .order_by(Appointment.start_at.desc())
        .all()
    )


def list_staff_appointments(staff_id: int):
    return (
        Appointment.query
        .filter_by(staff_id=staff_id)
        .order_by(Appointment.start_at.desc())
        .all()
    )


def list_business_appointments(business_id: int):
    return (
        Appointment.query
        .filter_by(business_id=business_id)
        .order_by(Appointment.start_at.desc())
        .all()
    )


def get_appointment_or_404(appointment_id: int):
    return Appointment.query.get_or_404(appointment_id)


def _ensure_customer_owns_appointment(appointment, user_id: int):
    if appointment.user_id != user_id:
        abort(403)


def _ensure_staff_owns_appointment(appointment, staff_id: int):
    if appointment.staff_id != staff_id:
        abort(403)


def _ensure_business_owns_appointment(appointment, business_id: int):
    if appointment.business_id != business_id:
        abort(403)


def _status_transition(appointment, status: str):
    appointment.status = status
    if status == "cancelled":
        appointment.cancelled_at = datetime.utcnow()

    db.session.add(appointment)
    db.session.commit()
    return appointment


def cancel_appointment_as_customer(appointment_id: int, user_id: int):
    appointment = get_appointment_or_404(appointment_id)
    _ensure_customer_owns_appointment(appointment, user_id)

    if appointment.status not in ("pending", "confirmed"):
        raise ValueError("A foglalás már nem mondható le.")

    return _status_transition(appointment, "cancelled")


def cancel_appointment_as_staff(appointment_id: int, staff_id: int):
    appointment = get_appointment_or_404(appointment_id)
    _ensure_staff_owns_appointment(appointment, staff_id)

    if appointment.status not in ("pending", "confirmed"):
        raise ValueError("A foglalás már nem mondható le.")

    return _status_transition(appointment, "cancelled")


def confirm_appointment_as_staff(appointment_id: int, staff_id: int):
    appointment = get_appointment_or_404(appointment_id)
    _ensure_staff_owns_appointment(appointment, staff_id)

    if appointment.status not in ("pending", "confirmed"):
        raise ValueError("A foglalás nem erősíthető meg.")

    return _status_transition(appointment, "confirmed")


def complete_appointment_as_staff(appointment_id: int, staff_id: int):
    appointment = get_appointment_or_404(appointment_id)
    _ensure_staff_owns_appointment(appointment, staff_id)

    if appointment.status != "confirmed":
        raise ValueError("Csak megerősített foglalás jelölhető készre.")

    return _status_transition(appointment, "completed")


def cancel_appointment_as_business(appointment_id: int, business_id: int):
    appointment = get_appointment_or_404(appointment_id)
    _ensure_business_owns_appointment(appointment, business_id)
    return _status_transition(appointment, "cancelled")


def confirm_appointment_as_business(appointment_id: int, business_id: int):
    appointment = get_appointment_or_404(appointment_id)
    _ensure_business_owns_appointment(appointment, business_id)
    return _status_transition(appointment, "confirmed")


def complete_appointment_as_business(appointment_id: int, business_id: int):
    appointment = get_appointment_or_404(appointment_id)
    _ensure_business_owns_appointment(appointment, business_id)
    return _status_transition(appointment, "completed")