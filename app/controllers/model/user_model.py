import hashlib
import secrets

class UserModel:
    def __init__(self, db):
        self.db = db
    
    def create_user(self, username, email, password, role='user'):
        # Verificar si el usuario ya existe
        if self.get_user_by_username(username):
            raise ValueError("Erabiltzaile izena dagoeneko existitzen da")
        
        if self.get_user_by_email(email):
            raise ValueError("Posta elektronikoa dagoeneko erregistratuta dago")
        
        # Hash de la contraseña
        password_hash = self._hash_password(password)
        
        query = """
        INSERT INTO users (username, email, password_hash, role, is_approved, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        user_id = self.db.execute_query(query, (username, email, password_hash, role, 0, 1))
        return user_id
    
    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = ? AND is_active = 1"
        return self.db.get_one(query, (username,))
    
    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = ? AND is_active = 1"
        return self.db.get_one(query, (email,))
    
    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = ? AND is_active = 1"
        return self.db.get_one(query, (user_id,))
    
    def verify_password(self, username, password):
        user = self.get_user_by_username(username)
        if not user:
            return None
        
        password_hash = self._hash_password(password)
        if user['password_hash'] == password_hash:
            return dict(user)
        return None
    
    def update_user(self, user_id, **kwargs):
        if not kwargs:
            return
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(user_id)
        
        query = f"UPDATE users SET {set_clause} WHERE id = ?"
        self.db.execute_query(query, values)
    
    def delete_user(self, user_id):
        query = "UPDATE users SET is_active = 0 WHERE id = ?"
        self.db.execute_query(query, (user_id,))
    
    def get_pending_users(self):
        query = "SELECT * FROM users WHERE is_approved = 0 AND is_active = 1"
        rows = self.db.execute_query(query)
        return [dict(row) for row in rows] if rows else []
    
    def approve_user(self, user_id):
        query = "UPDATE users SET is_approved = 1 WHERE id = ?"
        self.db.execute_query(query, (user_id,))
    
    def get_all_users(self):
        query = "SELECT * FROM users WHERE is_active = 1"
        rows = self.db.execute_query(query)
        return [dict(row) for row in rows] if rows else []
    
    def get_user_role(self, user_id):
        user = self.get_user_by_id(user_id)
        return user['role'] if user else None
    
    def _hash_password(self, password):
        """Hash simple de contraseña (en producción usar bcrypt)"""
        salt = "mi_salt_secreto"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def generate_session_token(self):
        return secrets.token_urlsafe(32)
