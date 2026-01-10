from flask import Flask
from config import Config
from app.database.connection import DatabaseConnection
from app.controllers.auth_controller import auth_blueprint
from app.controllers.admin_controller import admin_blueprint
from app.controllers.pokedex_controller import pokedex_blueprint
# --- NUEVO: Importar team_blueprint ---
from app.controllers.team_controller import team_blueprint
from app.controllers.notifications_controller import notifications_blueprint
from app.controllers.friend_controller import friend_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar DB
    db = DatabaseConnection()
    
    # Registrar blueprints
    app.register_blueprint(auth_blueprint())
    app.register_blueprint(admin_blueprint())
    # --- NUEVO: Registrar team_blueprint ---
    app.register_blueprint(team_blueprint()) 
    app.register_blueprint(pokedex_blueprint())
    app.register_blueprint(notifications_blueprint())
    app.register_blueprint(friend_blueprint())
    app.secret_key = Config.SECRET_KEY
    
    return app