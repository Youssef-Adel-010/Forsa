from flask import Blueprint, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/sayHello', methods=['GET'])
def say_hello():
  age = request.json['age']
  return f'age is {age}', 200

