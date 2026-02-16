from flask import jsonify
from app.responses.error_response import ErrorsResponse

def register_error_handlers(app):
  def create_error_response(status_code, message, details):
    return jsonify(ErrorsResponse(status_code, message, details).to_dict()), status_code

  @app.errorhandler(404)
  def handle_404(error):
    return create_error_response(404,
      'Not Found',
      error.description if hasattr(error, 'description') and error.description else
      'The requested resource was not found.')

  @app.errorhandler(401)
  def handle_401(error):
    return create_error_response(401,
      'Unauthorized',
      error.description if hasattr(error, 'description') and error.description else
      'The authentication credentials received are not authorized.')

  @app.errorhandler(403)
  def handle_403(error):
    return create_error_response(403,
      'Forbidden',
      error.description if hasattr(error, 'description') and error.description else
      'The server understood the request, but will not fulfill it.')

  @app.errorhandler(400)
  def handle_400(error):
    return create_error_response(400,
      'Bad Request',
      error.description if hasattr(error, 'description') and error.description else
      'Modify or correct your request.')

  @app.errorhandler(415)
  def handle_415(error):
    return create_error_response(415,
      'Unsupported Media Type',
      'Couldn\'t load json data, check your request body and try again.')

  @app.errorhandler(405)
  def handle_405(error):
    return create_error_response(405,
      'Method Not Allowed',
      'Check HTTP method and try again.')

  @app.errorhandler(409)
  def handle_409(error):
    return create_error_response(409,
      'Conflict',
      error.description if hasattr(error, 'description') and error.description else
      'A conflict occurred with existing data.')

  @app.errorhandler(500)
  def handle_500(error):
    return create_error_response(500,
      'Internal Server Error',
      error.description if hasattr(error, 'description') and error.description else
      'An unexpected error occurred.')

  @app.errorhandler(422)
  def handle_422(error):
    return create_error_response(422,
      'Unprocessable Entity',
      error.description if hasattr(error, 'description') and error.description else
      'The server understood the content type of the request content, and the syntax of the request content was correct, but it was unable to process the contained instructions. may be a validation errors.')

  @app.errorhandler(423)
  def handle_423(error):
    return create_error_response(423,
      'Locked',
      error.description if hasattr(error, 'description') and error.description else
      'Your account is locked. Please activate your account to proceed.')

  @app.errorhandler(429)
  def handle_423(error):
    return create_error_response(423,
      'Too Many Requests',
      f'You sent too many requests in a given amount of time.')