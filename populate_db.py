import pokebase as pb
import sqlite3
from app.database.connection import DatabaseConnection

def populate():
    print("🚀 Hasieratzen Pokédex betetzea (Cargando Pokédex)...")
    
    # 1. Conexión manual para este script
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 2. Asegurar que existe la Generación 1 (Belaunaldi)
    # Requisito de tu Foreign Key
    try:
        cursor.execute("INSERT OR IGNORE INTO Belaunaldi (Zenbakia) VALUES (1)")
        conn.commit()
    except Exception as e:
        print(f"Error creando generación: {e}")

    # 3. Recorrer los primeros 151 Pokémon (Gen 1)
    for i in range(1, 152):
        try:
            # Pedir a la API (Esto tarda un poco porque descarga de internet)
            pokemon = pb.pokemon(i)
            print(f"📥 Deskargatzen: {pokemon.name} ({i}/151)...")

            # Datos básicos
            poke_id = pokemon.id
            nombre = pokemon.name.capitalize() # Poner primera mayúscula
            altura = pokemon.height / 10.0     # La API lo da en decímetros
            peso = pokemon.weight / 10.0       # La API lo da en hectogramos
            
            # Imagen (Sprite oficial)
            imagen = pokemon.sprites.front_default

            # Estadísticas (El orden en la API suele ser: hp, attack, defense, special-attack, special-defense, speed)
            stats = {s.stat.name: s.base_stat for s in pokemon.stats}
            ps = stats.get('hp', 0)
            eraso = stats.get('attack', 0)
            defentsa = stats.get('defense', 0)
            defentsa_esp = stats.get('special-defense', 0)
            abiadura = stats.get('speed', 0)

            # --- INSERTAR POKÉMON ---
            cursor.execute("""
                INSERT OR REPLACE INTO Pokemon_Pokedex 
                (PokemonID, Izena, Altuera, Pisua, Irudia, PS, Eraso, Defentsa, Defentsa_esp, Abiadura, BelaunaldiaZenbakia)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (poke_id, nombre, altura, peso, imagen, ps, eraso, defentsa, defentsa_esp, abiadura))

            # --- GESTIONAR TIPOS (MOTA) ---
            for type_slot in pokemon.types:
                tipo_nombre = type_slot.type.name.capitalize()
                
                # 1. Insertar el Tipo si no existe en la tabla Mota
                cursor.execute("INSERT OR IGNORE INTO Mota (Izena) VALUES (?)", (tipo_nombre,))
                
                # 2. Relacionar Pokémon con Tipo
                cursor.execute("""
                    INSERT OR IGNORE INTO Pokemon_Pokedex_Mota (PokemonID, MotaIzena)
                    VALUES (?, ?)
                """, (poke_id, tipo_nombre))

            conn.commit()

        except Exception as e:
            print(f"❌ Errorea {i} (ID)-rekin: {e}")

    conn.close()
    print("✅ Pokédex completada con éxito!")

if __name__ == '__main__':
    populate()