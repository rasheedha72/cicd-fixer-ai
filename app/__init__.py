from flask import Flask
from .routes import views

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'

    app.register_blueprint(views)

    return app
