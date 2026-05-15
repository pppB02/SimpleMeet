from ....db_models import Business, UserAccount
import base64
from slugify import slugify

def generate_public_id(business_id:int,business_name:str):
    b = base64.b64encode(f"{business_name}{business_id}".encode()).decode("utf-8")
    print("New public ID:",b)
    return b

class FinishSetup():
    def __init__(self,db,sessionData,admin_user_id):
        self.admin_user_id = admin_user_id
        self.db = db

        self.name = sessionData['name']
        self.website = sessionData['website']
        self.categories = sessionData['categories']
        self.location = sessionData['location']
    
    def checkData(self):
        existing_name = Business.query.filter_by(
            name=self.name).first()
        
        if existing_name:
            raise ValueError(f"Ez a név már foglalt! FS")
        
        existing_admin = Business.query.filter_by(
            id=self.admin_user_id).first()
        
        if existing_admin:
            raise ValueError(f"Ehhez a fiókhoz már regisztráltak üzletet! FS")

    def SaveData(self):
        newBusiness = Business(name=self.name,
                               website=self.website,
                               categories=self.categories,
                               location=self.location,
                               admin_user_id=self.admin_user_id,
                               slug=slugify(self.name),
                               public_id="GEN")
        
        admin_user = UserAccount.query.get(self.admin_user_id)
        admin_user.has_business = True

        print("slug",newBusiness.slug)

        try:
            self.db.session.add(newBusiness)
            self.db.session.flush()

            newBusiness.public_id = generate_public_id(newBusiness.id,newBusiness.name)
            print(f"http://localhost:5000/a/{newBusiness.slug}-{newBusiness.public_id}")

            self.db.session.add(newBusiness)
            self.db.session.commit()
            print("Business data saved")
            
            return None
        except Exception as e:
            raise e