import datetime
from app import db
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Enrollment(db.Model):
  __tablename__ = "enrollments"

  # Columns
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
  watched_videos = Column(Integer, default=0, nullable=False)
  progress = Column(Integer, default=0, nullable=False)
  is_completed = Column(Boolean, default=False, nullable=False)
  enrolled_at = Column(DateTime, default=func.now, nullable=False)

  # Indexes
  __table_args__ = (
    UniqueConstraint("user_id", "course_id", name="uq_user_course"),
    Index("ix_user_course", "user_id", "course_id"),
  )

  # Relations
  user = relationship("User", back_populates="enrollments")
  course = relationship("Course", back_populates="enrollments")
