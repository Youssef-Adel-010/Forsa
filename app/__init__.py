from pathlib import Path
from flask import Flask, json
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize extension objects; these are bound to the app in `create_app()`.
db = SQLAlchemy()
migrate = Migrate()
cors = CORS(resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager()


def create_app():
  # Application factory: creates and configures the Flask app instance.
  app = Flask(__name__)

  # Error handlers are registered to format errors consistently across the app.
  from app.handlers.error_handlers import register_error_handlers
  register_error_handlers(app)

  # JWT helpers (callbacks) are registered so JWT behaviors are centralized.
  from app.handlers.jwt_handlers import register_jwt_helper
  register_jwt_helper(jwt)

  # Load configuration from `config.json` placed alongside this file.
  app.config.from_file(Path(__file__).resolve().parent/'config.json', load = json.load)

  # Import models so that they are registered with SQLAlchemy metadata.
  from app.models import user
  from app.models import application
  from app.models import enrollment
  from app.models import job
  from app.models import course
  from app.models import blocklist

  # Register blueprints (API routes)
  from app.routes.auth_routes import auth_bp
  app.register_blueprint(auth_bp, url_prefix='/api/auth')

  # Bind extensions to the app instance
  db.init_app(app)
  migrate.init_app(app, db)
  cors.init_app(app)
  jwt.init_app(app)

  return app
