import datetime
from sqlalchemy import *
from app import db
from sqlalchemy.orm import relationship

class Application(db.Model):
  __tablename__ = "applications"

  # Columns
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
  applied_at = Column(DateTime, default=func.now, nullable=False)
  status = Column(String(50), nullable=False)

  # Indexes
  __table_args__ = (
    UniqueConstraint("user_id", "job_id", name="uq_user_job"),
    Index("ix_user_job", "user_id", "job_id"),
  )

  # Relations
  user = relationship("User", back_populates="applications")
  job = relationship("Job", back_populates="applications")
