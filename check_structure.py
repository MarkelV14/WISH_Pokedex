import sqlite3

def check_structure():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    print("--- TAULAK ---")
    # Datu-basean dauden taula guztien izenak lortu
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    for t in tables:
        print(f"- {t[0]}")

    print("\n--- POKEMON_POKEDEX ZUTABEAK ---")
    # Pokemon_Pokedex taularen zutabeak ikusi (ea hemen dauden 'Mota1', 'Type1' edo antzekoak)
    try:
        columns = cursor.execute("PRAGMA table_info(Pokemon_Pokedex);").fetchall()
        for c in columns:
            print(f"- {c[1]}") # Zutabearen izena
    except:
        print("Ezin izan da Pokemon_Pokedex irakurri.")

    conn.close()

if __name__ == '__main__':
    check_structure()