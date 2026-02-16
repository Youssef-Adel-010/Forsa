from app import db
from sqlalchemy import Column, String

class Blocklist(db.Model):
  __tablename__ = 'blocklist'

  # Columns
  jti = Column(String, primary_key=True)
