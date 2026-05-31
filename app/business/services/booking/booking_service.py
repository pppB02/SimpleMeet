from datetime import timedelta

from sqlalchemy import and_

from app import db
from ....db_models import Appointment, Business, Service, Staff


def create_appointment(
    user_id: int,
    business_id: int,
    service_id: int,
    staff_id: int,
    start_at,
    notes: str | None = None,
):
    business = Business.query.get_or_404(business_id)
    service = Service.query.get_or_404(service_id)
    staff = Staff.query.get_or_404(staff_id)

    if service.business_id != business.id:
        raise ValueError("A szolgáltatás nem ehhez az üzlethez tartozik.")

    if staff.business_id != business.id:
        raise ValueError("A kiválasztott munkatárs nem ehhez az üzlethez tartozik.")

    if service not in staff.services:
        raise ValueError("A kiválasztott munkatárs nem végzi ezt a szolgáltatást.")

    end_at = start_at + timedelta(minutes=service.duration)

    conflict = Appointment.query.filter(
        Appointment.staff_id == staff_id,
        Appointment.status.in_(["pending", "confirmed"]),
        and_(
            Appointment.start_at < end_at,
            Appointment.end_at > start_at,
        ),
    ).first()

    if conflict:
        raise ValueError("Ez az időpont már foglalt.")

    appointment = Appointment(
        user_id=user_id,
        business_id=business_id,
        service_id=service_id,
        staff_id=staff_id,
        start_at=start_at,
        end_at=end_at,
        notes=notes,
        status="confirmed",
    )

    db.session.add(appointment)
    db.session.commit()
    return appointment