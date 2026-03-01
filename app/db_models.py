from app import db
from datetime import datetime


# ======================
# USER ACCOUNT
# ======================

class UserAccount(db.Model):
    __tablename__ = "user_account"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum('customer', 'staff', 'business_admin'),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship("Customer", back_populates="user", uselist=False)
    staff = db.relationship("Staff", back_populates="user", uselist=False)
    business = db.relationship("Business", back_populates="admin", uselist=False)

    def __repr__(self):
        return f"<UserAccount {self.email} ({self.role})>"


# ======================
# BUSINESS
# ======================

class Business(db.Model):
    __tablename__ = "business"

    business_id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))

    admin_user_id = db.Column(
        db.Integer,
        db.ForeignKey("user_account.user_id"),
        unique=True
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    admin = db.relationship("UserAccount", back_populates="business")
    staff_members = db.relationship("Staff", back_populates="business", cascade="all, delete")
    services = db.relationship("Service", back_populates="business", cascade="all, delete")

    def __repr__(self):
        return f"<Business {self.business_name}>"


# ======================
# STAFF
# ======================

class Staff(db.Model):
    __tablename__ = "staff"

    staff_id = db.Column(db.Integer, primary_key=True)

    business_id = db.Column(
        db.Integer,
        db.ForeignKey("business.business_id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user_account.user_id"),
        unique=True
    )

    business = db.relationship("Business", back_populates="staff_members")
    user = db.relationship("UserAccount", back_populates="staff")

    availabilities = db.relationship("Availability", back_populates="staff", cascade="all, delete")
    appointments = db.relationship("Appointment", back_populates="staff", cascade="all, delete")

    def __repr__(self):
        return f"<Staff {self.user_id}>"


# ======================
# CUSTOMER
# ======================

class Customer(db.Model):
    __tablename__ = "customer"

    customer_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user_account.user_id"),
        unique=True
    )

    phone = db.Column(db.String(50))

    user = db.relationship("UserAccount", back_populates="customer")
    appointments = db.relationship("Appointment", back_populates="customer", cascade="all, delete")

    def __repr__(self):
        return f"<Customer {self.user_id}>"


# ======================
# SERVICE
# ======================

class Service(db.Model):
    __tablename__ = "service"

    service_id = db.Column(db.Integer, primary_key=True)

    business_id = db.Column(
        db.Integer,
        db.ForeignKey("business.business_id"),
        nullable=False
    )

    name = db.Column(db.String(255), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2))

    business = db.relationship("Business", back_populates="services")
    appointments = db.relationship("Appointment", back_populates="service", cascade="all, delete")

    def __repr__(self):
        return f"<Service {self.name} ({self.duration_minutes} min)>"


# ======================
# AVAILABILITY
# ======================

class Availability(db.Model):
    __tablename__ = "availability"

    availability_id = db.Column(db.Integer, primary_key=True)

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("staff.staff_id"),
        nullable=False
    )

    day_of_week = db.Column(db.Integer, nullable=False)  # 0-6
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    staff = db.relationship("Staff", back_populates="availabilities")

    def __repr__(self):
        return f"<Availability Staff:{self.staff_id} Day:{self.day_of_week}>"


# ======================
# APPOINTMENT
# ======================

class Appointment(db.Model):
    __tablename__ = "appointment"

    appointment_id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer.customer_id"),
        nullable=False
    )

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("staff.staff_id"),
        nullable=False
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("service.service_id"),
        nullable=False
    )

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    status = db.Column(
        db.Enum('booked', 'cancelled', 'completed'),
        default='booked'
    )

    customer = db.relationship("Customer", back_populates="appointments")
    staff = db.relationship("Staff", back_populates="appointments")
    service = db.relationship("Service", back_populates="appointments")

    def __repr__(self):
        return f"<Appointment {self.start_time} ({self.status})>"