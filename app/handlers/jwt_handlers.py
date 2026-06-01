from functools import wraps
from flask import jsonify
from flask_jwt_extended import JWTManager, current_user
from app.models.blocklist import Blocklist
from app.repositories.user_repository import UserRepository
from app.responses.error_response import ErrorsResponse
from app import db


def register_jwt_helper(jwt: JWTManager):
  def create_error_response(status_code, message, details):
    response = ErrorsResponse(
      status_code=status_code,
      details=details,
      message=message
    )
    return response.to_dict(), status_code

  @jwt.user_lookup_loader
  def user_lookup(_jwt_headers, jwt_data):
    # Given JWT data, return associated user instance.
    identity = jwt_data['sub']
    user = UserRepository.get_by_username(identity)
    return user

  @jwt.token_in_blocklist_loader
  def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return db.session.query(Blocklist).filter_by(jti=jti).one_or_none() is not None

  @jwt.revoked_token_loader
  def revoked_token(jwt_header, jwt_payload):
    return create_error_response(403, 'Forbidden', 'Token has been revoked, try to login again.')

  @jwt.expired_token_loader
  def expired_token(jwt_header, jwt_data):
    return create_error_response(401, 'Unauthorized Access', 'Expired token.')

  @jwt.invalid_token_loader
  def invalid_token(error):
    return create_error_response(401, 'Unauthorized Access', 'Invalid token.')

  @jwt.unauthorized_loader
  def unauthorized_loader(error):
    return create_error_response(401, 'Unauthorized Access', 'Missing or invalid token.')


def admin_required(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    if not current_user or not current_user.is_admin:
      error_response = ErrorsResponse(
        status_code=403,
        details="Admin access required",
        message="Forbidden"
      )
      return jsonify(error_response.to_dict()), 403
    return fn(*args, **kwargs)
  return wrapper

