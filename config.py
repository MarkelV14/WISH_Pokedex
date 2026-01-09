import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    DB_PATH = os.path.join(BASE_DIR, "database.db")
    SECRET_KEY = "supersecretkey"  # En producción, usa variable de entorno
    SESSION_TYPE = "filesystem"
