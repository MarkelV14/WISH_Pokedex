import sqlite3

def fix_evolutions():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    print("🧬 Eboluzioak datu-basean eguneratzen...")

    # Hiztegi honek esaten du: { NOR : NORI_EBOLUZIONATZEN_DUEN }
    # Adibidez: 1 (Bulbasaur) -> 2 (Ivysaur)
    # Soilik 151.raino daudenak jarri ditut.
    evolutions = {
        1: 2, 2: 3,        # Bulbasaur familia
        4: 5, 5: 6,        # Charmander familia
        7: 8, 8: 9,        # Squirtle familia
        10: 11, 11: 12,    # Caterpie
        13: 14, 14: 15,    # Weedle
        16: 17, 17: 18,    # Pidgey
        19: 20,            # Rattata
        21: 22,            # Spearow
        23: 24,            # Ekans
        25: 26,            # Pikachu
        27: 28,            # Sandshrew
        29: 30, 30: 31,    # Nidoran F
        32: 33, 33: 34,    # Nidoran M
        35: 36,            # Clefairy
        37: 38,            # Vulpix
        39: 40,            # Jigglypuff
        41: 42,            # Zubat
        43: 44, 44: 45,    # Oddish
        46: 47,            # Paras
        48: 49,            # Venonat
        50: 51,            # Diglett
        52: 53,            # Meowth
        54: 55,            # Psyduck
        56: 57,            # Mankey
        58: 59,            # Growlithe
        60: 61, 61: 62,    # Poliwag
        63: 64, 64: 65,    # Abra
        66: 67, 67: 68,    # Machop
        69: 70, 70: 71,    # Bellsprout
        72: 73,            # Tentacool
        74: 75, 75: 76,    # Geodude
        77: 78,            # Ponyta
        79: 80,            # Slowpoke
        81: 82,            # Magnemite
        84: 85,            # Doduo
        86: 87,            # Seel
        88: 89,            # Grimer
        90: 91,            # Shellder
        92: 93, 93: 94,    # Gastly
        96: 97,            # Drowzee
        98: 99,            # Krabby
        100: 101,          # Voltorb
        102: 103,          # Exeggcute
        104: 105,          # Cubone
        109: 110,          # Koffing
        111: 112,          # Rhyhorn
        116: 117,          # Horsea
        118: 119,          # Goldeen
        120: 121,          # Staryu
        129: 130,          # Magikarp
        133: 134,          # Eevee (Vaporeon jartzen dugu adibidez, bat edukitzeko)
        138: 139,          # Omanyte
        140: 141,          # Kabuto
        147: 148, 148: 149 # Dratini
    }

    try:
        count = 0
        for current_id, next_id in evolutions.items():
            # SQL: Eguneratu PokemonID hau, EboluzioaID hori jarriz
            cursor.execute("UPDATE Pokemon_Pokedex SET EboluzioaID = ? WHERE PokemonID = ?", (next_id, current_id))
            count += 1
            
        conn.commit()
        print(f"✅ {count} Pokemon eguneratu dira eboluzioekin!")
        print("Orain zure iragazkiak funtzionatu beharko luke.")
        
    except Exception as e:
        print(f"Errorea: {e}")
    
    conn.close()

if __name__ == '__main__':
    fix_evolutions()