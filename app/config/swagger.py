SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Forsa API Documentation",
        "description": "API documentation for the Forsa platform, including Auth, Courses, Jobs, and Profile management.",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Access Token in the Authorization header. Example: \"Authorization: Bearer {access_token}\""
        }
    }
}


SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
