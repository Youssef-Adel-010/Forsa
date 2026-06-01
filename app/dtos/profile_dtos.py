from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class ProfileCourseDto(BaseModel):
    course_id: int
    title: str
    category: str
    level: str
    instructor: str
    progress: int
    is_completed: bool


class ProfileJobDto(BaseModel):
    job_id: int
    title: str
    company: str
    location: str
    status: str
    applied_at: str


class ProfileResponseDto(BaseModel):
    id: int
    name: str
    username: str
    email: str
    phone: str
    summary: Optional[str] = None
    cv_path: str
    enrolled_courses: List[ProfileCourseDto]
    applied_jobs: List[ProfileJobDto]


class ProfileUpdateDto(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=11, max_length=11)
    summary: Optional[str] = Field(None, min_length=1, max_length=500)

    @field_validator("phone")
    def validate_phone(cls, val: Optional[str]):
        if val is not None and not val.isdigit():
            raise ValueError("Phone must contain 11 digits.")
        return val
