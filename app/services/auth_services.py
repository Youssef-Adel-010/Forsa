from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app.dtos.signup_dto import SignupDto
from app.dtos.login_dto import LoginDto
from app.dtos.user_response_dto import UserResponseDto
from app.models.user import User
from app.models.blocklist import Blocklist
from app.repositories.user_repository import UserRepository
from app import db


class AuthServices:

  @staticmethod
  def signup(dto: SignupDto) -> UserResponseDto:
    """
    Register a new user with validation and persistence.
    
    Flow:
    1. Validate that username, email, and phone don't already exist
    2. Hash the password using werkzeug
    3. Create User model instance
    4. Persist to database via repository
    5. Return formatted UserResponseDto
    
    Args:
        dto (SignupDto): Validated signup data (already validated by Pydantic)
    
    Returns:
        UserResponseDto: New user profile data
    
    Raises:
        ValueError: If user with same username/email/phone exists or DB error
    """
    if UserRepository.user_exists_by_username(dto.username):
      raise ValueError("Username already exists")
    
    if UserRepository.user_exists_by_email(dto.email):
      raise ValueError("Email already exists")
    
    if UserRepository.user_exists_by_phone(dto.phone):
      raise ValueError("Phone number already exists")
    
    password_hash = generate_password_hash(dto.password, method='pbkdf2:sha256')
    
    new_user = User(
      name=dto.name,
      username=dto.username,
      email=dto.email,
      phone=dto.phone,
      summary=dto.summary,
      password_hash=password_hash,
      cv_path=dto.cv_path,
      is_admin=False
    )
    
    created_user = UserRepository.create(new_user)
    
    return UserResponseDto(
      id=created_user.id,
      name=created_user.name,
      username=created_user.username,
      email=created_user.email,
      phone=created_user.phone,
      summary=created_user.summary,
      cv_path=created_user.cv_path,
      created_at=created_user.created_at
    )

  @staticmethod
  def login(dto: LoginDto) -> dict:
    """
    Authenticate user and generate JWT tokens.
    
    Flow:
    1. Find user by username or email
    2. Verify password hash
    3. Generate access and refresh JWT tokens
    4. Return tokens and user data
    
    Args:
        dto (LoginDto): Login credentials (username/email + password)
    
    Returns:
        dict: Contains access_token, refresh_token, and user data
    
    Raises:
        ValueError: If user not found or password incorrect
    """
    user = UserRepository.get_by_username(dto.username)
    if not user:
      user = UserRepository.get_by_email(dto.username)
    
    if not user:
      raise ValueError("Invalid username/email or password")
    
    if not check_password_hash(user.password_hash, dto.password):
      raise ValueError("Invalid username/email or password")
    
    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)
    
    user_response = UserResponseDto(
      id=user.id,
      name=user.name,
      username=user.username,
      email=user.email,
      phone=user.phone,
      summary=user.summary,
      cv_path=user.cv_path,
      created_at=user.created_at
    )
    
    return {
      'access_token': access_token,
      'refresh_token': refresh_token,
      'user': user_response.model_dump()
    }

  @staticmethod
  def logout(jti: str) -> None:
    """
    Revoke a JWT token by adding it to the blocklist.
    
    Args:
        jti (str): JWT Token ID from token claims
    
    Returns:
        None
    """
    blocklist_entry = Blocklist(jti=jti)
    db.session.add(blocklist_entry)
    db.session.commit()

  @staticmethod
  def refresh_access_token(identity: str) -> str:
    """
    Generate a new access token from refresh token.
    
    Args:
        identity (str): User identity from refresh token
    
    Returns:
        str: New access token
    """
    access_token = create_access_token(identity=identity)
    return access_token