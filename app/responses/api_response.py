class ApiResponse:
  def __init__(self,
    status_code,
    message,
    data=None):
    self.status_code = status_code
    self.message = message
    self.data = data

  def to_dict(self):
    response = {
        'status_code': self.status_code,
        'success': True,
        'message': self.message,
        'data': self.data
    }
    if not response['data']: response.pop('data')
    return response