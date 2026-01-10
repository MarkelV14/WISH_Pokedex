import sqlite3

def check_db_types():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    print("--- ZURE DATU-BASEKO MOTAK ---")
    try:
        # Ikusi zein mota dauden gordeta
        rows = cursor.execute("SELECT Izena FROM Mota").fetchall()
        for row in rows:
            print(f"'{row[0]}'") # Komatxo artean inprimatu espazioak ikusteko
    except Exception as e:
        print(f"Errorea: {e}")
    
    conn.close()

if __name__ == '__main__':
    check_db_types()