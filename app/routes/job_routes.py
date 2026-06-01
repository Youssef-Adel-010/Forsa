from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from pydantic import ValidationError
from app.services.job_services import JobServices
from app.responses.api_response import ApiResponse
from app.handlers.jwt_handlers import admin_required
from app.dtos.job_dtos import CreateJobDto

job_bp = Blueprint('job', __name__)


@job_bp.post("")
@jwt_required()
@admin_required
def create_job():
    """
    Create a new job listing (admin only).
    ---
    tags:
      - Jobs (Admin)
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - company
            - category
            - type
            - description
            - requirements
            - salary
            - location
            - experience_level
          properties:
            title:
              type: string
            company:
              type: string
            category:
              type: string
            type:
              type: string
            description:
              type: string
            requirements:
              type: string
            salary:
              type: number
            location:
              type: string
            experience_level:
              type: string
    responses:
      201:
        description: Job created successfully
      400:
        description: Bad Request (validation error)
      403:
        description: Forbidden (admin access required)
      401:
        description: Unauthorized (missing or invalid token)
      500:
        description: Internal Server Error
    """
    try:
        data = request.get_json()
        job_dto = CreateJobDto(**data)

        created_job = JobServices.create_job(job_dto)

        response = ApiResponse(
            status_code=201,
            message="Job created successfully",
            data=created_job.model_dump()
        )
        return jsonify(response.to_dict()), 201
    except ValidationError as e:
        return jsonify({
            'status_code': 400,
            'success': False,
            'message': 'Bad Request',
            'details': str(e)
        }), 400
    except ValueError as e:
        return jsonify({
            'status_code': 400,
            'success': False,
            'message': 'Bad Request',
            'details': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'status_code': 500,
            'success': False,
            'message': 'Internal Server Error',
            'details': str(e)
        }), 500


@job_bp.get("")
@jwt_required(optional=True)
def list_jobs():
    """
    List all available jobs.
    ---
    tags:
      - Jobs
    security:
      - Bearer: []
    responses:
      200:
        description: List of available jobs retrieved successfully.
      500:
        description: Internal Server Error
    """
    try:
        user_id = current_user.id if current_user else None
        jobs = JobServices.list_jobs(user_id=user_id)

        response = ApiResponse(
            status_code=200,
            message="Jobs retrieved successfully",
            data=[j.model_dump() for j in jobs]
        )
        return jsonify(response.to_dict()), 200
    except Exception as e:
        return jsonify({
            'status_code': 500,
            'success': False,
            'message': 'Internal Server Error',
            'details': str(e)
        }), 500


@job_bp.get("/<int:job_id>")
@jwt_required(optional=True)
def get_job_details(job_id):
    """
    Get detailed summary of a specific job.
    ---
    tags:
      - Jobs
    security:
      - Bearer: []
    parameters:
      - name: job_id
        in: path
        type: integer
        required: true
        description: ID of the job listing
    responses:
      200:
        description: Job details retrieved successfully
      404:
        description: Job not found
      500:
        description: Internal Server Error
    """
    try:
        user_id = current_user.id if current_user else None
        details = JobServices.get_job_details(job_id, user_id=user_id)

        response = ApiResponse(
            status_code=200,
            message="Job details retrieved successfully",
            data=details.model_dump()
        )
        return jsonify(response.to_dict()), 200
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            return jsonify({
                'status_code': 404,
                'success': False,
                'message': 'Not Found',
                'details': error_msg
            }), 404
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


@job_bp.post("/<int:job_id>/apply")
@jwt_required()
def apply_to_job(job_id):
    """
    Apply for a specific job. Uses authenticated user profile data (no extra form).
    ---
    tags:
      - Jobs
    security:
      - Bearer: []
    parameters:
      - name: job_id
        in: path
        type: integer
        required: true
        description: ID of the job listing to apply to
    responses:
      201:
        description: Applied to job successfully
      404:
        description: Job not found
      409:
        description: Conflict (already applied to this job)
      401:
        description: Unauthorized (missing or invalid token)
      500:
        description: Internal Server Error
    """
    try:
        user_id = current_user.id
        app_info = JobServices.apply_to_job(job_id, user_id)

        response = ApiResponse(
            status_code=201,
            message="Applied to job successfully",
            data=app_info
        )
        return jsonify(response.to_dict()), 201
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            return jsonify({
                'status_code': 404,
                'success': False,
                'message': 'Not Found',
                'details': error_msg
            }), 404
        if "already applied" in error_msg.lower():
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
