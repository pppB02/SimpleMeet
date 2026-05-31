from app import db
from ...db_models import Service, Staff


def addMembersToServie(members: list[Staff], ServiceId: int):
    service = Service.query.filter_by(id=ServiceId).first()

    if not service:
        raise ValueError("Service not found")

    try:
        for member in members:
            if service not in member.services:
                member.services.append(service)

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e


def addServie(datas: dict):
    newService = Service(**datas)
    try:
        db.session.add(newService)
        db.session.flush()
        db.session.commit()
        return newService.id
    except Exception as e:
        db.session.rollback()
        raise e