import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class SignupDto(BaseModel):
  # DTO for signup payload validation using pydantic.
  # Fields include basic user properties and a `cv_path` where the uploaded CV is stored.
  name: str = Field(min_length=2, max_length=255)
  username: str = Field(min_length=3, max_length=255)
  email: EmailStr
  phone: str = Field(min_length=11, max_length=11)
  password: str = Field(min_length=8)
  summary: Optional[str] = Field(default=None, max_length=500)
  cv_path: str

  @field_validator("password")
  def validate_password(cls, val:str):
    # Ensure password contains at least one letter and one digit.
    pattern = r'^(?=.*[a-zA-Z])(?=.*\d).{8,}$'
    if not re.match(pattern, val):
      raise ValueError("Password must be more than 8 chars, contain at least one english letter and one digit.")
    return val


  @field_validator("phone")
  def validate_phone(cls, val:str):
    # Phone must be numeric (11 digits expected by business rules).
    if not val.isdigit():
      raise ValueError("Phone must contain 11 digits.")
    return val
