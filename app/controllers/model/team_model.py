class TeamModel:
    def __init__(self, db):
        self.db = db

    def has_team(self, user_id):
        """Verifica si el usuario ya tiene algún Pokémon en su equipo."""
        query = "SELECT COUNT(*) as count FROM Pokemon_Talde WHERE user_id = ?"
        result = self.db.get_one(query, (user_id,))
        return result['count'] > 0

    def get_pokemon_by_name(self, pokemon_name):
        """Busca el ID del Pokémon en la Pokédex por su nombre (insensible a mayúsculas)"""
        query = "SELECT * FROM Pokemon_Pokedex WHERE LOWER(Izena) = LOWER(?)"
        return self.db.get_one(query, (pokemon_name,))

    def add_pokemon_to_team(self, user_id, pokemon_id, nickname=None):
        """Añade el Pokémon al equipo"""
        query = """
        INSERT INTO Pokemon_Talde (user_id, Pokemon_PokedexID, Izena, Estatistikak_Guztira)
        VALUES (?, ?, ?, 0)
        """
        self.db.execute_query(query, (user_id, pokemon_id, nickname))

    def get_user_team(self, user_id):
        """Devuelve la lista de Pokémon que el usuario tiene actualmente en su equipo"""
        query = """
        SELECT pt.id, pt.user_id, pt.Pokemon_PokedexID, pt.Izena, pp.Irudia 
        FROM Pokemon_Talde pt
        JOIN Pokemon_Pokedex pp ON pt.Pokemon_PokedexID = pp.PokemonID
        WHERE pt.user_id = ?
        """
        return self.db.execute_query(query, (user_id,))
    
    def count_team_members(self, user_id):
        """Cuenta cuántos Pokémon tiene el equipo"""
        query = "SELECT COUNT(*) as count FROM Pokemon_Talde WHERE user_id = ?"
        res = self.db.get_one(query, (user_id,))
        return res['count']

    def get_all_pokemon_names(self):
        """Devuelve solo los nombres de todos los Pokémon para el autocompletado"""
        query = "SELECT Izena FROM Pokemon_Pokedex ORDER BY Izena ASC"
        return self.db.execute_query(query)

    
    def delete_pokemon_from_team(self, user_id, team_entry_id):
        """Ezabatu Pokémon bat taldetik (Elimina un Pokémon específico del equipo)"""
        # Usamos tanto el ID de la entrada como el user_id por seguridad
        # (para que nadie borre los Pokémon de otro usuario)
        query = "DELETE FROM Pokemon_Talde WHERE id = ? AND user_id = ?"
        self.db.execute_query(query, (team_entry_id, user_id))