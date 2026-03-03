from app import db
from app.models.user import User


class UserRepository:

  # Repository providing simple DB access methods for `User` model.
  @staticmethod
  def get_by_username(username: str):
    # Return the first user matching `username`.
    User.query.filter_by(username=username).first()

  @staticmethod
  def get_by_email(email: str):
    # Return the first user matching `email`.
    User.query.filter_by(username=email).first()

  @staticmethod
  def create(user: User):
    # Persist a new user instance and commit the transaction.
    db.session.add(user)
    db.session.commit()
