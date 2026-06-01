from pydantic import BaseModel, Field


class LoginDto(BaseModel):
  username: str = Field(min_length=1, description="Username or email")
  password: str = Field(min_length=1, description="User password")
