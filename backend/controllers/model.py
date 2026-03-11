from controllers.database import db
import enum
import uuid
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password

user_roles = sa.Table(
    "user_roles",
    db.Model.metadata,
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id"))
)

class CompanyApprovalStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class DriveStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"

class ApplicationStatus(enum.Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"

class Role(db.Model, RoleMixin):
    __tablename__ = "roles"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), unique=True, nullable=False)
    description = sa.Column(sa.String(255))

    users = so.relationship("User",secondary=user_roles,back_populates="roles")

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    username=sa.Column(sa.String(32),nullable=False,unique=True)
    email = sa.Column(sa.String(255), nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    active = sa.Column(sa.Boolean, default=True)
    fs_uniquifier = sa.Column(sa.String(255), unique=True, nullable=False)
    fs_token_uniquifier = sa.Column(sa.String(255), unique=True, nullable=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    roles = so.relationship("Role",secondary=user_roles,back_populates="users")

    student = so.relationship("Student", back_populates="user", uselist=False)
    company = so.relationship("Company", back_populates="user", uselist=False)

class Student(db.Model):
    __tablename__ = "students"

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), unique=True)
    name = sa.Column(sa.String(64),nullable=False)
    roll_number = sa.Column(sa.String(50), unique=True, nullable=False)
    department = sa.Column(sa.String(100))
    cgpa = sa.Column(sa.Float)
    resume = sa.Column(sa.String(255))
    passing_out_year = sa.Column(sa.Integer)

    user = so.relationship("User", back_populates="student")
    applications = so.relationship("Application", back_populates="student")

class Company(db.Model):
    __tablename__ = "companies"

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), unique=True)

    company_name = sa.Column(sa.String(200), nullable=False)
    hr_contact = sa.Column(sa.String(100))
    website = sa.Column(sa.String(200))
    approval_status = sa.Column(
        sa.Enum(CompanyApprovalStatus), default=CompanyApprovalStatus.PENDING
    )
    user = so.relationship("User", back_populates="company")
    drives = so.relationship("PlacementDrive", back_populates="company")

class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"

    id = sa.Column(sa.Integer, primary_key=True)
    company_id = sa.Column(sa.Integer, sa.ForeignKey("companies.id"))

    title = sa.Column(sa.String(200), nullable=False)
    description = sa.Column(sa.Text)

    min_cgpa = sa.Column(sa.Float)
    passing_out_year = sa.Column(sa.Integer)
    
    application_deadline = sa.Column(sa.DateTime)
    status = sa.Column(sa.Enum(DriveStatus), default=DriveStatus.PENDING)

    company = so.relationship("Company", back_populates="drives")
    applications = so.relationship("Application", back_populates="drive")
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

class Application(db.Model):
    __tablename__ = "applications"
    __table_args__ = (
        sa.UniqueConstraint("student_id", "drive_id", name="uq_student_drive"),
    )

    id = sa.Column(sa.Integer, primary_key=True)
    student_id = sa.Column(sa.Integer, sa.ForeignKey("students.id"))
    drive_id = sa.Column(sa.Integer, sa.ForeignKey("placement_drives.id"))

    applied_on = sa.Column(sa.DateTime, default=datetime.utcnow)
    status = sa.Column(sa.Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)

    student = so.relationship("Student", back_populates="applications")
    drive = so.relationship("PlacementDrive", back_populates="applications")


