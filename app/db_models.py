from app import db
from datetime import datetime
from flask_login import UserMixin


# ======================
# USER ACCOUNT
# ======================

class UserAccount(db.Model, UserMixin):
    __tablename__ = 'user_account'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.Enum('customer', 'staff', 'business_admin', name='role_enum'),
        default="customer",
        nullable=False
    )

    has_business = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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

    categories = db.Column(
        db.Enum(
            "barber-shop",
            "hair-salon",
            "finger-nail",
            "spa",
            name="business_category_enum"
        ),
        nullable=False
    )

    admin_user_id = db.Column(
        db.Integer,
        db.ForeignKey('user_account.id'),
        nullable=False
    )

    public_id = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)

    staff_members = db.relationship('Staff', backref='employer', lazy=True)
    service = db.relationship('Service', backref='service_provider', lazy=True)
    appointments = db.relationship('Appointment', backref='business_item', lazy=True)


# ======================
# STAFF <-> SERVICE M2M
# ======================

staff_service = db.Table(
    'staff_service',
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
)


# ======================
# STAFF
# ======================

class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    # many-to-many relationship a szolgáltatásokhoz
    services = db.relationship(
        'Service',
        secondary=staff_service,
        backref='staff_members',
        lazy=True
    )

    pfp_name = db.Column(db.String(255), nullable=False)

    days = db.relationship('Day', backref='staff_member', lazy=True)
    appointments = db.relationship('Appointment', backref='staff_member', lazy=True)


# ======================
# SERVICE
# ======================

class Service(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    serviceType = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    price = db.Column(db.Integer, nullable=False, default=0)
    duration = db.Column(db.Integer, nullable=False, default=30)
    price_type = db.Column(db.Enum("Fixed", name="price_type_enum"), default="Fixed", nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    appointments = db.relationship('Appointment', backref='service_item', lazy=True)


# ======================
# APPOINTMENT
# ======================

class Appointment(db.Model):
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)

    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)

    # új booking logika
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)

    status = db.Column(
        db.Enum(
            'pending',
            'confirmed',
            'cancelled',
            'completed',
            'no_show',
            name='appointment_status_enum'
        ),
        default='confirmed',
        nullable=False
    )

    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cancelled_at = db.Column(db.DateTime)

    # kompatibilitás a régi kóddal
    arrival_time = db.Column(db.Time)
    complete_time = db.Column(db.Time)


# ======================
# DAY
# ======================

class Day(db.Model):
    __tablename__ = 'day'

    id = db.Column(db.BigInteger, primary_key=True)
    staff_id = db.Column(db.BigInteger, db.ForeignKey('staff.id'), nullable=False)
    name = db.Column(db.String(50))
    open_time = db.Column(db.Time)
    close_time = db.Column(db.Time)
    booked_appointment = db.Column(db.JSON)


# ======================
# OPENING HOUR
# ======================

class OpeningHour(db.Model):
    __tablename__ = 'opening_hour'

    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer)  # 0 = hétfő, 6 = vasárnap
    open_time = db.Column(db.Time)
    close_time = db.Column(db.Time)
    is_closed = db.Column(db.Boolean, default=False, nullable=False)

    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    business = db.relationship("Business", backref="opening_hours")


# ======================
# STAFF INVITE LINKS
# ======================

class StaffIviteLinks(db.Model):
    __tablename__ = 'staff_invite_links'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    token = db.Column(db.String(255))