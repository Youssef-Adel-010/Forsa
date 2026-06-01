import os
import uuid
from flask import Blueprint, current_app, jsonify, request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.dtos.signup_dto import SignupDto
from app.dtos.login_dto import LoginDto
from app.services.auth_services import AuthServices
from app.responses.api_response import ApiResponse
from app.responses.error_response import ErrorsResponse


auth_bp = Blueprint('auth', __name__)


def allowed_file(filename: str) -> bool:
  """Check if uploaded file has an allowed extension."""
  return "." in filename and \
    filename.rsplit(".", 1)[1].lower() in current_app.config.get("ALLOWED_EXTENSIONS", ["pdf", "doc", "docx"])


@auth_bp.post("/signup")
def signup():
  """
  Register a new user with CV file upload.
  ---
  tags:
    - Authentication
  consumes:
    - multipart/form-data
  parameters:
    - name: name
      in: formData
      type: string
      required: true
      description: The full name of the user
    - name: username
      in: formData
      type: string
      required: true
      description: Unique username
    - name: email
      in: formData
      type: string
      required: true
      description: Valid email address
    - name: phone
      in: formData
      type: string
      required: true
      description: 11-digit phone number
    - name: password
      in: formData
      type: string
      required: true
      description: Password (min 8 chars, 1 letter, 1 digit)
    - name: summary
      in: formData
      type: string
      required: true
      description: Brief professional summary
    - name: cv
      in: formData
      type: file
      required: true
      description: CV file (PDF, DOC, DOCX)
  responses:
    201:
      description: User registered successfully
    400:
      description: Bad Request (missing fields or invalid file type)
    409:
      description: Conflict (username, email or phone already exists)
    422:
      description: Unprocessable Entity (validation failed)
    500:
      description: Internal Server Error
  """
  try:
    data = request.form.to_dict()
    file = request.files.get("cv")

    if not file or file.filename == '':
      return jsonify({
        'status_code': 400,
        'success': False,
        'message': 'Bad Request',
        'details': 'CV file is required'
      }), 400

    if not allowed_file(file.filename):
      return jsonify({
        'status_code': 400,
        'success': False,
        'message': 'Bad Request',
        'details': 'Invalid file type. Allowed: pdf, doc, docx'
      }), 400

    upload_folder = current_app.config.get("UPLOAD_FOLDER", "static/cvs")
    os.makedirs(upload_folder, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    data["cv_path"] = filepath

    dto = SignupDto(**data)

    user = AuthServices.signup(dto)

    response = ApiResponse(
      status_code=201,
      message="User registered successfully",
      data=user.model_dump()
    )
    return jsonify(response.to_dict()), 201

  except ValidationError as e:
    errors = []
    for error in e.errors():
      errors.append({
        'field': '.'.join(str(x) for x in error['loc']),
        'message': error['msg']
      })
    return jsonify({
      'status_code': 422,
      'success': False,
      'message': 'Unprocessable Entity',
      'details': 'Validation failed',
      'errors': errors
    }), 422

  except ValueError as e:
    error_msg = str(e)
    if "already exists" in error_msg:
      try:
        if 'filepath' in locals() and os.path.exists(filepath):
          os.remove(filepath)
      except:
        pass
      return jsonify({
        'status_code': 409,
        'success': False,
        'message': 'Conflict',
        'details': error_msg
      }), 409
    else:
      try:
        if 'filepath' in locals() and os.path.exists(filepath):
          os.remove(filepath)
      except:
        pass
      return jsonify({
        'status_code': 400,
        'success': False,
        'message': 'Bad Request',
        'details': error_msg
      }), 400

  except Exception as e:
    try:
      if 'filepath' in locals() and os.path.exists(filepath):
        os.remove(filepath)
    except:
      pass

    return jsonify({
      'status_code': 500,
      'success': False,
      'message': 'Internal Server Error',
      'details': str(e)
    }), 500


@auth_bp.post("/login")
def login():
  """
  Authenticate user and return JWT tokens.
  ---
  tags:
    - Authentication
  parameters:
    - name: credentials
      in: body
      required: true
      schema:
        type: object
        required:
          - username
          - password
        properties:
          username:
            type: string
            description: Username or email
          password:
            type: string
            description: Password
  responses:
    200:
      description: Login successful, returns tokens and user profile
    400:
      description: Bad Request
    401:
      description: Unauthorized (Invalid username/email or password)
    422:
      description: Unprocessable Entity (validation failed)
    500:
      description: Internal Server Error
  """
  try:
    data = request.get_json()

    if not data:
      return jsonify({
        'status_code': 400,
        'success': False,
        'message': 'Bad Request',
        'details': 'Request body is required'
      }), 400

    dto = LoginDto(**data)

    tokens = AuthServices.login(dto)

    response = ApiResponse(
      status_code=200,
      message="Login successful",
      data={
        'access_token': tokens['access_token'],
        'refresh_token': tokens['refresh_token'],
        'user': tokens['user']
      }
    )
    return jsonify(response.to_dict()), 200

  except ValidationError as e:
    errors = []
    for error in e.errors():
      errors.append({
        'field': '.'.join(str(x) for x in error['loc']),
        'message': error['msg']
      })
    return jsonify({
      'status_code': 422,
      'success': False,
      'message': 'Unprocessable Entity',
      'details': 'Validation failed',
      'errors': errors
    }), 422

  except ValueError as e:
    error_msg = str(e)
    if "Invalid" in error_msg:
      return jsonify({
        'status_code': 401,
        'success': False,
        'message': 'Unauthorized',
        'details': error_msg
      }), 401
    else:
      return jsonify({
        'status_code': 400,
        'success': False,
        'message': 'Bad Request',
        'details': error_msg
      }), 400

  except Exception as e:
    return jsonify({
      'status_code': 500,
      'success': False,
      'message': 'Internal Server Error',
      'details': str(e)
    }), 500


@auth_bp.post("/logout")
@jwt_required()
def logout():
  """
  Revoke current JWT token by adding to blocklist.
  ---
  tags:
    - Authentication
  security:
    - Bearer: []
  responses:
    200:
      description: Logout successful
    401:
      description: Unauthorized (Missing or invalid token)
    500:
      description: Internal Server Error
  """
  try:
    # Get JWT claims
    jti = get_jwt()['jti']

    # Add token to blocklist
    AuthServices.logout(jti)

    # Return success response
    response = ApiResponse(
      status_code=200,
      message="Logout successful"
    )
    return jsonify(response.to_dict()), 200

  except Exception as e:
    return jsonify({
      'status_code': 500,
      'success': False,
      'message': 'Internal Server Error',
      'details': str(e)
    }), 500


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
  """
  Generate a new access token using refresh token.
  ---
  tags:
    - Authentication
  security:
    - Bearer: []
  responses:
    200:
      description: Access token refreshed successfully
    401:
      description: Unauthorized (Invalid or expired refresh token)
    500:
      description: Internal Server Error
  """
  try:
    identity = get_jwt_identity()
    access_token = AuthServices.refresh_access_token(identity)

    response = ApiResponse(
      status_code=200,
      message="Access token refreshed",
      data={'access_token': access_token}
    )
    return jsonify(response.to_dict()), 200

  except Exception as e:
    return jsonify({
      'status_code': 500,
      'success': False,
      'message': 'Internal Server Error',
      'details': str(e)
    }), 500
