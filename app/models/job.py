import datetime
from app import db
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Job(db.Model):
  __tablename__ = "jobs"

  # Columns
  id = Column(Integer, primary_key=True)
  title = Column(String(255), nullable=False)
  company = Column(String(255), nullable=False)
  category = Column(String(255), nullable=False)
  type = Column(String(100), nullable=False)
  description = Column(String(2000), nullable=False)
  requirements = Column(String(2000), nullable=False)
  salary = Column(DECIMAL(10, 2), nullable=False)
  location = Column(String(255), nullable=False)
  experience_level = Column(String(100), nullable=False)
  created_at = Column(DateTime, default=func.now, nullable=False)

  # Relations
  applications = relationship(
    "Application",
    back_populates="job",
    cascade="all, delete-orphan"
  )
