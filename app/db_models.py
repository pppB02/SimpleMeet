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
    has_business = db.Column(db.Boolean, nullable=False, default=False)
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
    public_id = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)

    # Kapcsolatok
    staff_members = db.relationship('Staff', backref='employer', lazy=True)
    service = db.relationship('Service', backref='service_provider', lazy=True)

# ======================
# STAFF
# ======================

staff_service = db.Table(
    "staff_service",
    db.Column("staff_id", db.Integer, db.ForeignKey("staff.id"), primary_key=True),
    db.Column("service_id", db.Integer, db.ForeignKey("service.id"), primary_key=True),
)

class Staff(db.Model):
    __tablename__ = "staff"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_account.id"), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    pfp_name = db.Column(db.String(255), nullable=False)

    services = db.relationship("Service", secondary=staff_service, backref="staff_members")

# ======================
# SERVICE
# ======================

class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)

    serviceType = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # perc
    price_type = db.Column(db.Enum("Fixed", name="price_type_enum"), default="Fixed")
    is_active = db.Column(db.Boolean, default=True, nullable=False)

# ======================
# APPOINTMENT
# ======================

class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user_account.id"), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)

    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)

    status = db.Column(
        db.Enum("pending", "confirmed", "cancelled", "completed", "no_show", name="appointment_status"),
        default="confirmed",
        nullable=False
    )

    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cancelled_at = db.Column(db.DateTime)

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

class OpeningHour(db.Model):
    __tablename__ = "opening_hour"

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0 = hétfő
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)
    is_closed = db.Column(db.Boolean, default=False, nullable=False)

class StaffIviteLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    token = db.Column(db.String(255))