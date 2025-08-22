from flask import Flask
from .models import init_db

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = './app/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit

    # Initialize DB
    init_db()

    # Import routes after app creation to avoid circular import
    from . import routes
    routes.init_app(app)

    return app
