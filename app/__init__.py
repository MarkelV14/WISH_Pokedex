from flask import Flask
from config import Config
from app.controllers.auth_controller import auth_blueprint
from app.controllers.admin_controller import admin_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Registrar blueprints
    app.register_blueprint(auth_blueprint())
    app.register_blueprint(admin_blueprint())
    
    return app
