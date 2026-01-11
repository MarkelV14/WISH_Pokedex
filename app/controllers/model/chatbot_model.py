class ChatbotModel:
    def __init__(self, db):
        self.db = db

    def get_best_from_my_team(self, user_id):
        """
        Zure 'Pokemon_Talde' taulan dauden Pokemonen artean
        estatistika total handiena duena lortu.
        """
        query = """
        SELECT p.*, (p.PS + p.Eraso + p.Defentsa + p.Abiadura + p.Defentsa_esp) as Totala
        FROM Pokemon_Pokedex p
        JOIN Pokemon_Talde t ON p.PokemonID = t.Pokemon_PokedexID
        WHERE t.user_id = ?
        ORDER BY Totala DESC
        LIMIT 1
        """
        return self.db.get_one(query, (user_id,))
    def get_pokemon_by_name(self, name_input):
        """
        Izena bilatu (Case Insensitive).
        GARRANTZITSUA: Ez dugu espazioak garbitzen.
        Erabiltzaileak ' Charmander' idazten badu, horrela bilatuko du
        eta ez du aurkituko (9. eskakizuna betetzeko).
        """
        query = "SELECT * FROM Pokemon_Pokedex WHERE LOWER(Izena) = LOWER(?)"
        return self.db.get_one(query, (name_input,))
    def get_all_pokemon_names(self):
        """Pokemon guztien izenak lortu autokonpletaturako"""
        query = "SELECT Izena FROM Pokemon_Pokedex ORDER BY Izena ASC"
        results = self.db.execute_query(query)
        # Zerrenda simple bat itzuli: ['Abra', 'Aerodactyl', ...]
        return [row['Izena'] for row in results]
    def get_pokemon_types(self, pokemon_id):
        """
        Pokemon baten motak lortu.
        Zure eskeman 'Pokemon_Pokedex_Mota' taulak zuzenean dauka 'MotaIzena'.
        Ez dugu JOIN-ik behar Mota taularekin izena lortzeko.
        """
        query = "SELECT MotaIzena FROM Pokemon_Pokedex_Mota WHERE PokemonID = ?"
        results = self.db.execute_query(query, (pokemon_id,))
        # Emaitza: ['Sua', 'Hegakaria']
        return [row['MotaIzena'] for row in results]

    def get_weaknesses(self, type_list):
        """
        Zein motaren aurka den AHULA (Nor den indartsua nire aurka).
        Taula: Indartsu_DA (MotaIndartsua, MotaAhula)
        Bilatzen dugu: Nor da 'MotaIndartsua' nire motak 'MotaAhula' direnean?
        """
        if not type_list: return []
        
        placeholders = ','.join('?' * len(type_list))
        
        # Indartsu_DA taulan zutabeak 'MotaIndartsua' eta 'MotaAhula' dira
        query = f"""
        SELECT DISTINCT MotaIndartsua 
        FROM Indartsu_DA 
        WHERE MotaAhula IN ({placeholders})
        """
        results = self.db.execute_query(query, tuple(type_list))
        return [row['MotaIndartsua'] for row in results]

    def get_strengths(self, type_list):
        """
        Zein motaren aurka den INDARTSUA (Nor den ahula nire aurka).
        Bilatzen dugu: Nor da 'MotaAhula' nire motak 'MotaIndartsua' direnean?
        """
        if not type_list: return []
        
        placeholders = ','.join('?' * len(type_list))
        
        query = f"""
        SELECT DISTINCT MotaAhula 
        FROM Indartsu_DA 
        WHERE MotaIndartsua IN ({placeholders})
        """
        results = self.db.execute_query(query, tuple(type_list))
        return [row['MotaAhula'] for row in results]
    def get_pokemon_by_id(self, pokemon_id):
        """ID baten bidez Pokemon baten datuak lortu (Eboluzioa bilatzeko)"""
        query = "SELECT * FROM Pokemon_Pokedex WHERE PokemonID = ?"
        return self.db.get_one(query, (pokemon_id,))