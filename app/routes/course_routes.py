from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from pydantic import ValidationError
from app.services.course_services import CourseServices
from app.responses.api_response import ApiResponse
from app.handlers.jwt_handlers import admin_required
from app.dtos.course_dtos import CreateCourseDto

course_bp = Blueprint('course', __name__)

@course_bp.post("")
@jwt_required()
@admin_required
def create_course():
    """
    Create a new course (admin only).
    ---
    tags:
      - Courses (Admin)
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
            - category
            - level
            - instructor
            - description
            - total_videos
            - duration_in_hours
            - youtube_playlist_id
          properties:
            title:
              type: string
            category:
              type: string
            level:
              type: string
            instructor:
              type: string
            description:
              type: string
            total_videos:
              type: integer
            duration_in_hours:
              type: integer
            youtube_playlist_id:
              type: string
    responses:
      201:
        description: Course created successfully
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
        course_dto = CreateCourseDto(**data)

        created_course = CourseServices.create_course(course_dto)

        response = ApiResponse(
            status_code=201,
            message="Course created successfully",
            data=created_course.model_dump()
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


@course_bp.get("")
@jwt_required(optional=True)
def list_courses():
    """
    List all available courses.
    ---
    tags:
      - Courses
    security:
      - Bearer: []
    responses:
      200:
        description: List of available courses retrieved successfully.
      500:
        description: Internal Server Error
    """
    try:
        user_id = current_user.id if current_user else None
        courses = CourseServices.list_courses(user_id=user_id)

        response = ApiResponse(
            status_code=200,
            message="Courses retrieved successfully",
            data=[c.model_dump() for c in courses]
        )
        return jsonify(response.to_dict()), 200
    except Exception as e:
        return jsonify({
            'status_code': 500,
            'success': False,
            'message': 'Internal Server Error',
            'details': str(e)
        }), 500


@course_bp.get("/<int:course_id>")
@jwt_required(optional=True)
def get_course_details(course_id):
    """
    Get detailed summary of a specific course.
    ---
    tags:
      - Courses
    security:
      - Bearer: []
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: ID of the course
    responses:
      200:
        description: Course details retrieved successfully
      404:
        description: Course not found
      500:
        description: Internal Server Error
    """
    try:
        user_id = current_user.id if current_user else None
        details = CourseServices.get_course_details(course_id, user_id=user_id)

        response = ApiResponse(
            status_code=200,
            message="Course details retrieved successfully",
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


@course_bp.post("/<int:course_id>/enroll")
@jwt_required()
def enroll_in_course(course_id):
    """
    Enroll the currently authenticated user in a course.
    ---
    tags:
      - Courses
    security:
      - Bearer: []
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: ID of the course to enroll in
    responses:
      201:
        description: Enrolled in course successfully
      404:
        description: Course not found
      409:
        description: Conflict (already enrolled in this course)
      401:
        description: Unauthorized (missing or invalid token)
      500:
        description: Internal Server Error
    """
    try:
        user_id = current_user.id
        enrollment_info = CourseServices.enroll_in_course(course_id, user_id)

        response = ApiResponse(
            status_code=201,
            message="Enrolled in course successfully",
            data=enrollment_info
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
        if "already enrolled" in error_msg.lower():
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


@course_bp.get("/<int:course_id>/content")
@jwt_required()
def get_course_content(course_id):
    """
    Access course content (playlist and videos) after enrollment.
    ---
    tags:
      - Courses
    security:
      - Bearer: []
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: ID of the course
    responses:
      200:
        description: Course content retrieved successfully
      403:
        description: Forbidden (user is not enrolled in this course)
      404:
        description: Course not found
      401:
        description: Unauthorized (missing or invalid token)
      500:
        description: Internal Server Error
    """
    try:
        user_id = current_user.id
        content = CourseServices.get_course_content(course_id, user_id)

        response = ApiResponse(
            status_code=200,
            message="Course content retrieved successfully",
            data=content.model_dump()
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
        if "not enrolled" in error_msg.lower():
            return jsonify({
                'status_code': 403,
                'success': False,
                'message': 'Forbidden',
                'details': error_msg
            }), 403
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


@course_bp.post("/<int:course_id>/videos/<int:video_index>/complete")
@jwt_required()
def complete_video(course_id, video_index):
    """
    Mark/Unmark a specific video as completed.
    ---
    tags:
      - Courses
    security:
      - Bearer: []
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: ID of the course
      - name: video_index
        in: path
        type: integer
        required: true
        description: 0-indexed position of the video in the playlist
      - name: body
        in: body
        required: false
        schema:
          type: object
          properties:
            completed:
              type: boolean
              default: true
              description: Set to true to complete the video, false to uncomplete
    responses:
      200:
        description: Video completion status updated successfully
      403:
        description: Forbidden (user is not enrolled in this course)
      404:
        description: Course not found
      400:
        description: Bad Request (invalid video index)
      401:
        description: Unauthorized (missing or invalid token)
      500:
        description: Internal Server Error
    """
    try:
        user_id = current_user.id

        # Parse optional JSON body
        completed = True
        if request.is_json:
            body = request.get_json(silent=True)
            if body and isinstance(body, dict):
                completed = body.get("completed", True)

        updated_content = CourseServices.update_video_completion(
            course_id=course_id,
            user_id=user_id,
            video_index=video_index,
            completed=completed
        )

        response = ApiResponse(
            status_code=200,
            message="Video completion status updated successfully",
            data=updated_content.model_dump()
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
        if "not enrolled" in error_msg.lower():
            return jsonify({
                'status_code': 403,
                'success': False,
                'message': 'Forbidden',
                'details': error_msg
            }), 403
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
