from typing import List, Optional
from pydantic import BaseModel, Field


class CreateCourseDto(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Course title")
    category: str = Field(..., min_length=1, max_length=255, description="Course category")
    level: str = Field(..., min_length=1, max_length=100, description="Course level (e.g., Beginner, Intermediate, Advanced)")
    instructor: str = Field(..., min_length=1, max_length=255, description="Instructor name")
    description: str = Field(..., min_length=1, max_length=1000, description="Course description")
    total_videos: int = Field(..., ge=1, description="Total number of videos in course")
    duration_in_hours: int = Field(..., ge=1, description="Total duration in hours")
    youtube_playlist_id: str = Field(..., min_length=1, max_length=255, description="YouTube playlist ID")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Python for Beginners",
                "category": "Programming",
                "level": "Beginner",
                "instructor": "John Doe",
                "description": "Learn Python programming from scratch",
                "total_videos": 50,
                "duration_in_hours": 20,
                "youtube_playlist_id": "PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
            }
        }


class CourseResponseDto(BaseModel):
    id: int
    title: str
    category: str
    level: str
    instructor: str
    description: str
    short_description: str
    total_videos: int
    duration_in_hours: int
    youtube_playlist_id: str
    is_enrolled: bool = False
    progress: int = 0
    is_completed: bool = False


class VideoResponseDto(BaseModel):
    index: int
    video_id: str
    title: str
    duration: str
    is_completed: bool


class CourseContentResponseDto(BaseModel):
    course_id: int
    title: str
    youtube_playlist_id: str
    progress: int
    is_completed: bool
    videos: List[VideoResponseDto]
