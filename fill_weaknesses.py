import sqlite3

def fill_weaknesses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    print("⚔️ Ahuleziak (Indartsu_DA taula) betetzen ingelesezko izenekin...")

    # 1. Taula garbitu
    cursor.execute("DELETE FROM Indartsu_DA")

    # 2. Erlazioak (Orain INGELESEZ, zure datu-basean bezala)
    # Egitura: (NOR_DEN_INDARTSUA, NOREN_AURKA)
    relationships = [
        # FIRE (Sua) -> Indartsua da hauen aurka:
        ('Fire', 'Grass'), ('Fire', 'Ice'), ('Fire', 'Bug'), ('Fire', 'Steel'),
        
        # WATER (Ura)
        ('Water', 'Fire'), ('Water', 'Ground'), ('Water', 'Rock'),
        
        # GRASS (Landarea)
        ('Grass', 'Water'), ('Grass', 'Ground'), ('Grass', 'Rock'),
        
        # ELECTRIC (Elektrikoa)
        ('Electric', 'Water'), ('Electric', 'Flying'),
        
        # ICE (Izotza)
        ('Ice', 'Grass'), ('Ice', 'Ground'), ('Ice', 'Flying'), ('Ice', 'Dragon'),
        
        # FIGHTING (Borroka)
        ('Fighting', 'Normal'), ('Fighting', 'Ice'), ('Fighting', 'Rock'), ('Fighting', 'Steel'),
        
        # POISON (Pozoitsua)
        ('Poison', 'Grass'), ('Poison', 'Fairy'), # Badaezpada biak (Poison ingelesez da zuzena)
        ('Poison', 'Grass'),
        
        # GROUND (Lurra)
        ('Ground', 'Fire'), ('Ground', 'Electric'), ('Ground', 'Poison'), ('Ground', 'Rock'), ('Ground', 'Steel'),
        
        # FLYING (Hegakaria)
        ('Flying', 'Grass'), ('Flying', 'Fighting'), ('Flying', 'Bug'),
        
        # PSYCHIC (Psikikoa)
        ('Psychic', 'Fighting'), ('Psychic', 'Poison'),
        
        # BUG (Zomorroa)
        ('Bug', 'Grass'), ('Bug', 'Psychic'),
        
        # ROCK (Harkaitza)
        ('Rock', 'Fire'), ('Rock', 'Ice'), ('Rock', 'Flying'), ('Rock', 'Bug'),
        
        # GHOST (Mamua)
        ('Ghost', 'Psychic'), ('Ghost', 'Ghost'),
        
        # DRAGON (Dragoia)
        ('Dragon', 'Dragon'),

        # STEEL (Altzairua)
        ('Steel', 'Ice'), ('Steel', 'Rock'), ('Steel', 'Fairy'),

        # FAIRY (Maitagarria)
        ('Fairy', 'Fighting'), ('Fairy', 'Dragon')
    ]

    try:
        # 'INSERT OR IGNORE' erabiltzen dugu erroreak saihesteko (adibidez, Fairy existitzen ez bada)
        cursor.executemany("INSERT OR IGNORE INTO Indartsu_DA (MotaIndartsua, MotaAhula) VALUES (?, ?)", relationships)
        conn.commit()
        print(f"✅ Erlazioak gehitu dira! ({len(relationships)} guztira)")
        print("Orain zure webgunera joaten bazara, ahuleziak agertu beharko lirateke.")
        
    except Exception as e:
        print(f"Errorea: {e}")

    conn.close()

if __name__ == '__main__':
    fill_weaknesses()