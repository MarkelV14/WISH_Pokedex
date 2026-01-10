class FriendModel:
    def __init__(self, db):
        self.db = db

    def get_followed_users(self, user_id):
        """Lortu nik jarraitzen ditudan erabiltzaileen zerrenda"""
        query = """
        SELECT u.id, u.username, u.email 
        FROM users u
        JOIN Lagunak l ON u.id = l.friend_id
        WHERE l.user_id = ?
        ORDER BY u.username ASC
        """
        return self.db.execute_query(query, (user_id,))

    def search_users_to_add(self, user_id, search_term):
        """
        Bilatu erabiltzaileak gehitzeko.
        BALDINTZAK:
        1. Izena 'search_term' antzekoa da.
        2. Ez naiz ni neu.
        3. Ez da jada nire laguna.
        4. Onartuta dago (is_approved = 1).
        """
        query = """
        SELECT id, username FROM users
        WHERE username LIKE ? 
        AND is_approved = 1
        AND id != ?
        AND id NOT IN (SELECT friend_id FROM Lagunak WHERE user_id = ?)
        """
        # % termino % formatua erabiltzen da bilaketa partzialerako
        term = f"%{search_term}%"
        return self.db.execute_query(query, (term, user_id, user_id))

    def add_friend(self, user_id, friend_id):
        """Lagun berria gehitu"""
        query = "INSERT OR IGNORE INTO Lagunak (user_id, friend_id) VALUES (?, ?)"
        self.db.execute_query(query, (user_id, friend_id))

    def remove_friend(self, user_id, friend_id):
        """Laguna ezabatu"""
        query = "DELETE FROM Lagunak WHERE user_id = ? AND friend_id = ?"
        self.db.execute_query(query, (user_id, friend_id))