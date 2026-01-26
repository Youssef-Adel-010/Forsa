import datetime
from app import db
from sqlalchemy import *
from sqlalchemy.orm import relationship

class User(db.Model):
  __tablename__ = "users"

  # Columns
  id = Column(Integer, primary_key=True)
  name = Column(String(255), nullable=False)
  username = Column(String(255), nullable=False, unique=True, index=True)
  email = Column(String(255), nullable=False, unique=True, index=True)
  phone = Column(String(50), nullable=False, unique=True, index=True)
  summary = Column(String(500))
  password_hash = Column(String(255), nullable=False)
  cv_path = Column(String(255), nullable=False)
  is_admin = Column(Boolean, default=False, nullable=False)
  created_at = Column(DateTime, default=func.now, nullable=False)

  # Relations
  enrollments = relationship(
    "Enrollment",
    back_populates="user",
    cascade="all, delete-orphan"
  )

  applications = relationship(
    "Application",
    back_populates="user",
    cascade="all, delete-orphan"
  )
