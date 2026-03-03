# Entry point for running the Flask application.
# It creates the app using the factory `create_app()` and runs it when executed directly.
from app import create_app

app = create_app()

if __name__ == '__main__':
  app.run()
