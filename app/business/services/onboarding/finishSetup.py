from datetime import datetime
import base64

from slugify import slugify

from ....db_models import Business, UserAccount


def generate_public_id(business_id: int, business_name: str):
    raw = f"{business_name}-{business_id}".encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")


class FinishSetup:
    def __init__(self, db, sessionData, admin_user_id):
        self.admin_user_id = int(admin_user_id)
        self.db = db

        self.name = sessionData["name"]
        self.website = sessionData.get("website")
        self.categories = sessionData["categories"]
        self.location = sessionData["location"]

    def checkData(self):
        existing_name = Business.query.filter_by(name=self.name).first()
        if existing_name:
            raise ValueError("Ez a név már foglalt!")

        existing_admin = Business.query.filter_by(admin_user_id=self.admin_user_id).first()
        if existing_admin:
            raise ValueError("Ehhez a fiókhoz már regisztráltak üzletet!")

    def SaveData(self):
        newBusiness = Business(
            name=self.name,
            website=self.website,
            categories=self.categories,
            location=self.location,
            admin_user_id=self.admin_user_id,
            slug=slugify(self.name),
            public_id="GEN",
        )

        admin_user = UserAccount.query.get(self.admin_user_id)
        if not admin_user:
            raise ValueError("Admin user not found")

        admin_user.has_business = True

        try:
            self.db.session.add(newBusiness)
            self.db.session.flush()

            pb = generate_public_id(newBusiness.id, newBusiness.name)
            print(pb,"nev business")
            newBusiness.public_id = pb

            self.db.session.add(newBusiness)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e