import datetime
import secrets

class AuthModel:
    def __init__(self, db):
        self.db = db
    
    def create_session(self, user_id, remember_me=False):
        token = secrets.token_urlsafe(32)
        
        if remember_me:
            expires_at = datetime.datetime.now() + datetime.timedelta(days=30)
        else:
            expires_at = datetime.datetime.now() + datetime.timedelta(hours=24)
        
        query = """
        INSERT INTO user_sessions (user_id, session_token, expires_at)
        VALUES (?, ?, ?)
        """
        
        self.db.execute_query(query, (user_id, token, expires_at))
        return token
    
    def validate_session(self, token):
        query = """
        SELECT us.*, u.username, u.email 
        FROM user_sessions us
        JOIN users u ON us.user_id = u.id
        WHERE us.session_token = ? 
        AND us.expires_at > datetime('now')
        AND u.is_active = 1
        """
        
        return self.db.get_one(query, (token,))
    
    def delete_session(self, token):
        query = "DELETE FROM user_sessions WHERE session_token = ?"
        self.db.execute_query(query, (token,))
    
    def delete_all_user_sessions(self, user_id):
        query = "DELETE FROM user_sessions WHERE user_id = ?"
        self.db.execute_query(query, (user_id,))
