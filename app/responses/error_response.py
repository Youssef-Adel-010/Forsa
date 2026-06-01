class ErrorsResponse:
  def __init__(self,
    status_code=None,
    message=None,
    details=None):
    self.details = details
    self.status_code = status_code
    self.message = message

  def to_dict(self):
    return {
      'status_code': self.status_code,
      'details': self.details,
      'success': False,
      'message': self.message
    }