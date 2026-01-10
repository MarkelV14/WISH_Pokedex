class PokedexModel:
    def __init__(self, db):
        self.db = db

    # ---------------------------------------------------------
    # 0. ESTATISTIKAK (DASHBOARD) - HAU FALTA ZEN!
    # ---------------------------------------------------------
    def get_counts(self, user_id):
        """Lortu harrapatutakoak eta totalak panelerako"""
        # Harrapatutakoak
        query_captured = "SELECT COUNT(*) as count FROM Harrapatu WHERE user_id = ?"
        captured = self.db.get_one(query_captured, (user_id,))
        
        # Guztiak
        query_total = "SELECT COUNT(*) as count FROM Pokemon_Pokedex"
        total = self.db.get_one(query_total)
        
        return {
            'captured': captured['count'] if captured else 0,
            'total': total['count'] if total else 0
        }

    # ---------------------------------------------------------
    # 1. HARRAPATU / FALTA DIREN LISTAK
    # ---------------------------------------------------------
    def get_captured_list(self, user_id):
        query = """
        SELECT p.* FROM Pokemon_Pokedex p
        JOIN Harrapatu h ON p.PokemonID = h.PokemonID
        WHERE h.user_id = ?
        ORDER BY p.PokemonID ASC
        """
        return self.db.execute_query(query, (user_id,))

    def get_missing_list(self, user_id):
        query = """
        SELECT p.* FROM Pokemon_Pokedex p
        WHERE p.PokemonID NOT IN (
            SELECT PokemonID FROM Harrapatu WHERE user_id = ?
        )
        ORDER BY p.PokemonID ASC
        """
        return self.db.execute_query(query, (user_id,))

    def mark_as_captured(self, user_id, pokemon_id):
        query = "INSERT OR IGNORE INTO Harrapatu (user_id, PokemonID) VALUES (?, ?)"
        self.db.execute_query(query, (user_id, pokemon_id))

    def unmark_captured(self, user_id, pokemon_id):
        query = "DELETE FROM Harrapatu WHERE user_id = ? AND PokemonID = ?"
        self.db.execute_query(query, (user_id, pokemon_id))

    # ---------------------------------------------------------
    # 2. BILATZAILEA (SEARCH)
    # ---------------------------------------------------------
    def get_all_types(self):
        query = "SELECT Izena FROM Mota ORDER BY Izena ASC"
        return self.db.execute_query(query)

    def get_all_generations(self):
        query = "SELECT Zenbakia FROM Belaunaldi ORDER BY Zenbakia ASC"
        return self.db.execute_query(query)

    def search_pokemon(self, name_filter=None, type_filter=None, gen_filter=None, evo_filter=None):
        query = "SELECT DISTINCT p.* FROM Pokemon_Pokedex p"
        params = []
        conditions = []

        # JOIN motentzat
        if type_filter and type_filter != "Guztiak":
            query += " JOIN Pokemon_Pokedex_Mota pm ON p.PokemonID = pm.PokemonID"
            conditions.append("pm.MotaIzena = ?")
            params.append(type_filter)

        # Baldintzak
        if name_filter:
            conditions.append("p.Izena LIKE ?")
            params.append(f"%{name_filter}%")
            
        if gen_filter and gen_filter != "Guztiak":
            conditions.append("p.BelaunaldiaZenbakia = ?")
            params.append(gen_filter)

        if evo_filter and evo_filter != "Guztiak":
            if evo_filter == "Bai":
                conditions.append("p.EboluzioaID IS NOT NULL")
            elif evo_filter == "Ez":
                conditions.append("p.EboluzioaID IS NULL")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY p.PokemonID ASC"
        return self.db.execute_query(query, tuple(params))

    # ---------------------------------------------------------
    # 3. XEHETASUNAK (DETAILS)
    # ---------------------------------------------------------
    def get_pokemon_by_id(self, pokemon_id):
        """Pokemon bakar baten datu guztiak lortu"""
        query = "SELECT * FROM Pokemon_Pokedex WHERE PokemonID = ?"
        return self.db.get_one(query, (pokemon_id,))

    def get_pokemon_types(self, pokemon_id):
        """Pokemon baten motak lortu"""
        query = "SELECT MotaIzena FROM Pokemon_Pokedex_Mota WHERE PokemonID = ?"
        results = self.db.execute_query(query, (pokemon_id,))
        return [row['MotaIzena'] for row in results]

    def get_weaknesses(self, type_list):
        """Ahuleziak kalkulatu"""
        if not type_list: return []
        placeholders = ','.join('?' * len(type_list))
        query = f"""
        SELECT DISTINCT MotaIndartsua 
        FROM Indartsu_DA 
        WHERE MotaAhula IN ({placeholders})
        """
        results = self.db.execute_query(query, tuple(type_list))
        return [row['MotaIndartsua'] for row in results]
    def get_strengths(self, type_list):
        """
        Nire motak (attacker) zein motaren aurka diren indartsuak (defender).
        """
        if not type_list: return []
        placeholders = ','.join('?' * len(type_list))
        
        # ORAIN ALDERANTZIZ GALDETZEN DUGU:
        # Zein da 'MotaAhula' (galtzailea) nire mota 'MotaIndartsua' denean?
        query = f"""
        SELECT DISTINCT MotaAhula 
        FROM Indartsu_DA 
        WHERE MotaIndartsua IN ({placeholders})
        """
        results = self.db.execute_query(query, tuple(type_list))
        return [row['MotaAhula'] for row in results]

    def get_evolution_family(self, pokemon_id):
        """Eboluzio katea lortu"""
        # 1. Bilatu Aita (Root)
        current_id = pokemon_id
        while True:
            query_prev = "SELECT PokemonID FROM Pokemon_Pokedex WHERE EboluzioaID = ?"
            prev = self.db.get_one(query_prev, (current_id,))
            if prev:
                current_id = prev['PokemonID']
            else:
                break 
        
        # 2. Bilatu Semeak (Chain)
        family_names = []
        while current_id:
            query_curr = "SELECT Izena, EboluzioaID FROM Pokemon_Pokedex WHERE PokemonID = ?"
            curr = self.db.get_one(query_curr, (current_id,))
            if curr:
                family_names.append(curr['Izena'])
                current_id = curr['EboluzioaID'] 
            else:
                break
        return family_names