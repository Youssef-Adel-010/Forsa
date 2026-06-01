from pathlib import Path
from flask import Flask, json
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
from app.config.swagger import SWAGGER_TEMPLATE, SWAGGER_CONFIG

db = SQLAlchemy()
migrate = Migrate()
cors = CORS(resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager()


def create_app():
  app = Flask(__name__)

  from app.handlers.error_handlers import register_error_handlers
  register_error_handlers(app)

  from app.handlers.jwt_handlers import register_jwt_helper
  register_jwt_helper(jwt)

  app.config.from_file(Path(__file__).resolve().parent/'config.json', load = json.load)

  from app.models import user
  from app.models import application
  from app.models import enrollment
  from app.models import job
  from app.models import course
  from app.models import blocklist

  from app.routes.auth_routes import auth_bp
  app.register_blueprint(auth_bp, url_prefix='/api/auth')

  from app.routes.course_routes import course_bp
  app.register_blueprint(course_bp, url_prefix='/api/courses')

  from app.routes.job_routes import job_bp
  app.register_blueprint(job_bp, url_prefix='/api/jobs')

  from app.routes.profile_routes import profile_bp
  app.register_blueprint(profile_bp, url_prefix='/api/profile')

  Swagger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)

  db.init_app(app)
  migrate.init_app(app, db)
  cors.init_app(app)
  jwt.init_app(app)

  return app
