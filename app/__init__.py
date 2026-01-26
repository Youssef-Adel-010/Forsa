from pathlib import Path
from flask import Flask, json
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
cors = CORS(resources={r"/api/*": {"origins": "*"}})

def create_app():
  app = Flask(__name__)

  # Configurations
  config_path = Path(__file__).resolve().parent / 'config.json'
  app.config.from_file(config_path, load = json.load)

  # Models
  from app.models import user
  from app.models import application
  from app.models import enrollment
  from app.models import job
  from app.models import course

  # Routes
  from app.routes.auth_routes import auth_bp
  app.register_blueprint(auth_bp)

  # Initialize Extensions
  db.init_app(app)
  migrate.init_app(app, db)
  cors.init_app(app)

  return app
