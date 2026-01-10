class MessageModel:
    def __init__(self, db):
        self.db = db

    def create_message(self, user_id, message_text):
        """Mezu berri bat sortu DBan"""
        query = "INSERT INTO Mezua (user_id, Mezua) VALUES (?, ?)"
        self.db.execute_query(query, (user_id, message_text))

    def get_all_messages(self):
        """Mezu guztiak lortu (Nireak eta besteenak), berrienak lehenengo"""
        query = """
        SELECT m.Mezua, m.Data, u.username 
        FROM Mezua m
        JOIN users u ON m.user_id = u.id
        ORDER BY m.Data DESC
        LIMIT 50
        """
        return self.db.execute_query(query)

    def get_my_messages(self, user_id):
        """Soilik nire mezuak lortu"""
        query = """
        SELECT m.Mezua, m.Data, u.username 
        FROM Mezua m
        JOIN users u ON m.user_id = u.id
        WHERE m.user_id = ?
        ORDER BY m.Data DESC
        LIMIT 50
        """
        return self.db.execute_query(query, (user_id,))