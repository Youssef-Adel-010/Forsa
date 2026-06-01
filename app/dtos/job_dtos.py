from pydantic import BaseModel, Field


class CreateJobDto(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Job title")
    company: str = Field(..., min_length=1, max_length=255, description="Company name")
    category: str = Field(..., min_length=1, max_length=255, description="Job category")
    type: str = Field(..., min_length=1, max_length=100, description="Job type (e.g., Full-time, Part-time, Contract)")
    description: str = Field(..., min_length=1, max_length=2000, description="Job description")
    requirements: str = Field(..., min_length=1, max_length=2000, description="Job requirements")
    salary: float = Field(..., ge=0, description="Salary amount")
    location: str = Field(..., min_length=1, max_length=255, description="Job location")
    experience_level: str = Field(..., min_length=1, max_length=100, description="Experience level (e.g., Junior, Mid-level, Senior)")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Senior Python Developer",
                "company": "Tech Company",
                "category": "Software Development",
                "type": "Full-time",
                "description": "We are looking for experienced Python developers",
                "requirements": "5+ years of Python experience",
                "salary": 150000,
                "location": "Remote",
                "experience_level": "Senior"
            }
        }


class JobResponseDto(BaseModel):
    id: int
    title: str
    company: str
    category: str
    type: str
    description: str
    requirements: str
    salary: float
    location: str
    experience_level: str
    has_applied: bool = False
