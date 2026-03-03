import datetime
from pydantic import BaseModel


class UserResponseDto(BaseModel):
    # DTO used to shape user objects returned to clients (read-only fields).
    id: int
    name: str
    username: str
    email: str
    phone: str
    summary: str | None
    cv_path: str
    created_at: datetime

