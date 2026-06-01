import os
import uuid
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from pydantic import ValidationError
from app.dtos.profile_dtos import ProfileUpdateDto
from app.services.profile_services import ProfileServices
from app.responses.api_response import ApiResponse

profile_bp = Blueprint('profile', __name__)


def allowed_file(filename: str) -> bool:
    """Check if uploaded CV file has an allowed extension."""
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in current_app.config.get("ALLOWED_EXTENSIONS", ["pdf", "doc", "docx"])


@profile_bp.get("")
@jwt_required()
def get_profile():
    """
    Get current user's profile details.
    ---
    tags:
      - Profile
    security:
      - Bearer: []
    responses:
      200:
        description: Profile details retrieved successfully (includes personal info, enrolled courses, applied jobs)
      401:
        description: Unauthorized (missing or invalid token)
      404:
        description: User not found
      500:
        description: Internal Server Error
    """
    try:
        user_id = current_user.id
        profile = ProfileServices.get_profile(user_id)

        response = ApiResponse(
            status_code=200,
            message="Profile retrieved successfully",
            data=profile.model_dump()
        )
        return jsonify(response.to_dict()), 200
    except ValueError as e:
        return jsonify({
            'status_code': 404,
            'success': False,
            'message': 'Not Found',
            'details': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'status_code': 500,
            'success': False,
            'message': 'Internal Server Error',
            'details': str(e)
        }), 500


@profile_bp.put("")
@jwt_required()
def update_profile():
    """
    Update personal information in user's profile.
    ---
    tags:
      - Profile
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: New name
            email:
              type: string
              format: email
              description: New email
            phone:
              type: string
              description: 11-digit phone number
            summary:
              type: string
              description: Brief professional summary
    responses:
      200:
        description: Profile updated successfully
      400:
        description: Bad Request
      401:
        description: Unauthorized (missing or invalid token)
      409:
        description: Conflict (email or phone already in use)
      422:
        description: Unprocessable Entity (validation failure)
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

        dto = ProfileUpdateDto(**data)

        user_id = current_user.id
        profile = ProfileServices.update_profile(user_id, dto)

        response = ApiResponse(
            status_code=200,
            message="Profile updated successfully",
            data=profile.model_dump()
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
        if "already exists" in error_msg.lower():
            return jsonify({
                'status_code': 409,
                'success': False,
                'message': 'Conflict',
                'details': error_msg
            }), 409
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


@profile_bp.post("/cv")
@jwt_required()
def update_cv():
    """
    Upload a new CV file and update the user's profile.
    ---
    tags:
      - Profile
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - name: cv
        in: formData
        type: file
        required: true
        description: The new CV file (PDF, DOC, DOCX)
    responses:
      200:
        description: CV updated successfully
      400:
        description: Bad Request (missing or invalid file type)
      401:
        description: Unauthorized (missing or invalid token)
      404:
        description: User not found
      500:
        description: Internal Server Error
    """
    try:
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

        user_id = current_user.id
        profile = ProfileServices.update_cv(user_id, filepath)

        response = ApiResponse(
            status_code=200,
            message="CV updated successfully",
            data=profile.model_dump()
        )
        return jsonify(response.to_dict()), 200

    except ValueError as e:
        return jsonify({
            'status_code': 404,
            'success': False,
            'message': 'Not Found',
            'details': str(e)
        }), 404

    except Exception as e:
        return jsonify({
            'status_code': 500,
            'success': False,
            'message': 'Internal Server Error',
            'details': str(e)
        }), 500
