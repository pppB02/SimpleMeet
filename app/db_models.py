from app import db
from datetime import datetime
from flask_login import UserMixin

# ======================
# USER ACCOUNT
# ======================

class UserAccount(db.Model,UserMixin):
    __tablename__ = 'user_account'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('customer', 'staff', 'business_admin'), default="customer")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Kapcsolatok
    appointments = db.relationship('Appointment', backref='user', lazy=True)
    managed_business = db.relationship('Business', backref='admin', uselist=False)
    staff_profile = db.relationship('Staff', backref='user_info', uselist=False)

# ======================
# BUSINESS
# ======================

class Business(db.Model):
    __tablename__ = 'business'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    website = db.Column(db.String(255))
    categories = db.Column(db.Enum("barber-shop","hair-salon","finger-nail","spa"))
    admin_user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)

    # Kapcsolatok
    staff_members = db.relationship('Staff', backref='employer', lazy=True)

# ======================
# STAFF
# ======================

class Staff(db.Model):
    __tablename__ = 'staff'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    services = db.Column(db.JSON)  # JSON formátumú szolgáltatás lista

    # Kapcsolatok
    days = db.relationship('Day', backref='staff_member', lazy=True)
    appointments = db.relationship('Appointment', backref='staff_member', lazy=True)

# ======================
# SERVICE
# ======================

class Service(db.Model):
    __tablename__ = 'service'
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.BigInteger)
    duration = db.Column(db.BigInteger) # 30 perc

# ======================
# APPOINTMENT
# ======================

class Appointment(db.Model):
    __tablename__ = 'appointment'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    staff_id = db.Column(db.BigInteger, db.ForeignKey('staff.id'), nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)
    complete_time = db.Column(db.Time, nullable=False)

# ======================
# DAY
# ======================

class Day(db.Model):
    __tablename__ = 'day'
    
    id = db.Column(db.BigInteger, primary_key=True)
    staff_id = db.Column(db.BigInteger, db.ForeignKey('staff.id'), nullable=False)
    name = db.Column(db.String(50)) # Pl. "Hétfő"
    open_time = db.Column(db.Time)
    close_time = db.Column(db.Time)
    booked_appointment = db.Column(db.JSON) # JSON lista a foglalt időpontokról