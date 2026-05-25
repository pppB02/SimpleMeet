from app import db
from ...db_models import Service,Staff

def addMembersToServie(members: list[Staff], ServiceId: int):
    service = Service.query.filter_by(id=ServiceId).first()

    if not service:
        raise ValueError("Service not found")

    try:
        for member in members:
            MemberServices = member.services or {}

            MemberServices[str(service.id)] = service.name
            member.services = MemberServices

            print(f"New service added")

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(e)
        raise

def addServie(datas:dict):
    newService = Service(**datas)
    try:
        db.session.add(newService)
        db.session.flush()
        db.session.commit()
        print("Service added and saved!")
        return newService.id
    except Exception as e:
        print(str(e))
        #db.session.rollback()
        