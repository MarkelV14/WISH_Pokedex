import sqlite3
from config import Config
import hashlib
import secrets

class DatabaseConnection:
    def __init__(self):
        self.connection = sqlite3.connect(
            Config.DB_PATH,
            check_same_thread=False
        )
        self.connection.row_factory = sqlite3.Row
        self.init_db()
    
    def init_db(self):
        with open('app/database/schema.sql') as f:
            self.connection.executescript(f.read())
        self.connection.commit()
    
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.lastrowid
        finally:
            cursor.close()
    
    def get_one(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        finally:
            cursor.close()
    
    def close(self):
        self.connection.close()
