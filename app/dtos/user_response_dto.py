from datetime import datetime
from pydantic import BaseModel


class UserResponseDto(BaseModel):
    id: int
    name: str
    username: str
    email: str
    phone: str
    summary: str | None
    cv_path: str
    created_at: datetime

