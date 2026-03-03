from app import db
from sqlalchemy import Column, String


class Blocklist(db.Model):
  # Stores JWT `jti` identifiers for revoked tokens (a simple token blocklist).
  __tablename__ = 'blocklist'

  # Columns
  jti = Column(String, primary_key=True)
