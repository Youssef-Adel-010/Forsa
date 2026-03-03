# Example/auth routes for signup (currently commented out).
# This file contains a sample `signup` endpoint showing how the app would:
# - validate the uploaded CV file
# - save the file to `UPLOAD_FOLDER`
# - construct a `SignupDto` and call `AuthServices.signup`
# The code is intentionally commented out; uncomment and adapt when enabling the route.
# import os
# import uuid
# from flask import Blueprint, current_app, jsonify, request
# from pydantic import ValidationError
# from app.dtos.signup_dto import SignupDto
# from app.services.auth_services import AuthServices

# auth_bp = Blueprint('auth', __name__)

# def allowed_file(filename):
#   return "." in filename and \
#     filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

# @auth_bp.post("/signup")
# def signup():
#   try:
#     data = request.form.to_dict()
#     file = request.files.get("cv")
#
#     if not file:
#       return jsonify({"error": "CV file is required"}), 400
#
#     if not allowed_file(file.filename):
#       return jsonify({"error": "Invalid file type"}), 400
#
#     # Generate unique filename
#     ext = file.filename.rsplit(".", 1)[1].lower()
#     filename = f"{uuid.uuid4()}.{ext}"
#     filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
#
#     file.save(filepath)
#
#     data["cv_path"] = filepath
#
#     dto = SignupDto(**data)
#
#     user = AuthServices.signup(dto)
#
#     return jsonify(user.dict()), 201
#
#   except ValidationError as e:
#       return jsonify({"errors": e.errors()}), 400
#
#   except ValueError as e:
#       return jsonify({"error": str(e)}), 400
# #   data = request.form.to_dict()
# #   file = request.files.get("cv")
#
# #   dto = SignupDto(**data)
# #   response = AuthServices.signup(dto).model_dump()
# #   return jsonify(response), 201
