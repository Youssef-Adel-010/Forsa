from app import db
from app.models.user import User


class UserRepository:

  @staticmethod
  def get_by_username(username: str) -> User | None:
    return User.query.filter_by(username=username).first()

  @staticmethod
  def get_by_email(email: str) -> User | None:
    return User.query.filter_by(email=email).first()

  @staticmethod
  def get_by_id(user_id: int) -> User | None:
    return User.query.get(user_id)

  @staticmethod
  def create(user: User) -> User:
    db.session.add(user)
    db.session.commit()
    return user

  @staticmethod
  def user_exists_by_username(username: str) -> bool:
    return User.query.filter_by(username=username).first() is not None

  @staticmethod
  def user_exists_by_email(email: str) -> bool:
    return User.query.filter_by(email=email).first() is not None

  @staticmethod
  def user_exists_by_phone(phone: str) -> bool:
    return User.query.filter_by(phone=phone).first() is not None
