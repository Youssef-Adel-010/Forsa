from flask import abort, current_app
from app.dtos.signup_dto import SignupDto
from app.dtos.user_response_dto import UserResponseDto
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthServices:

  # Service layer for authentication-related operations.
  # Methods here orchestrate validations, repository calls, and DTO mapping.
  @staticmethod
  def signup(dto: SignupDto):
    # Placeholder: accept a SignupDto and return a UserResponseDto (to be implemented).
    return UserResponseDto()

  @staticmethod
  def save_cv():
    # Placeholder for saving uploaded CVs using app config (e.g., UPLOAD_FOLDER).
    # current_app.config()
    pass