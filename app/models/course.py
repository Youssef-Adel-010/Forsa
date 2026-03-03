from sqlalchemy import *
from app import db
from sqlalchemy.orm import relationship


class Course(db.Model):
  # Represents an online course with metadata used for enrollment and display.
  __tablename__ = "courses"

  # Columns
  id = Column(Integer, primary_key=True)
  title = Column(String(255), nullable=False)
  category = Column(String(255), nullable=False)
  level = Column(String(100), nullable=False)
  instructor = Column(String(255), nullable=False)
  description = Column(String(1000), nullable=False)
  total_videos = Column(Integer, nullable=False)
  duration_in_hours = Column(Integer, nullable=False)
  youtube_playlist_id = Column(String(255), nullable=False)

  # Relations
  enrollments = relationship(
    "Enrollment",
    back_populates="course",
    cascade="all, delete-orphan"
  )
