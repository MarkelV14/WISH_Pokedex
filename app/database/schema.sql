-- ============================================================
-- 1. Tabla de Generaciones (Belaunaldi)
-- ============================================================
CREATE TABLE IF NOT EXISTS Belaunaldi (
    Zenbakia INTEGER PRIMARY KEY -- Número de la generación (ej. 1, 2, 3...)
);

-- ============================================================
-- 2. Tabla de Tipos (Mota)
-- ============================================================
CREATE TABLE IF NOT EXISTS Mota (
    Izena TEXT UNIQUE NOT NULL PRIMARY KEY, -- Nombre del tipo (Fuego, Agua...)
    Irudia TEXT                 -- URL o ruta de la imagen del tipo
);

-- ============================================================
-- 3. Tabla de la Pokédex (Pokemon_Pokedex)
-- Representa la especie del Pokémon (datos generales)
-- ============================================================
CREATE TABLE IF NOT EXISTS Pokemon_Pokedex (
    PokemonID INTEGER,   -- ID del Pokémon
    Izena TEXT UNIQUE NOT NULL,      -- Nombre (ej. Charmander)
    Altuera REAL,
    Pisua REAL,
    Irudia TEXT,
    PS INTEGER,                      -- Puntos de Salud base
    Eraso INTEGER,                   -- Ataque
    Defentsa INTEGER,                -- Defensa
    Defentsa_esp INTEGER,            -- Defensa Especial
    Abiadura INTEGER,                -- Velocidad
    
    -- Claves foráneas definidas en el documento
                 
    BelaunaldiaZenbakia INTEGER,
    EboluzioaID INTEGER,             -- ID del Pokémon relacionado por evolución (Pre-evolución)
    PRIMARY KEY (PokemonID),
    FOREIGN KEY (BelaunaldiaZenbakia) REFERENCES Belaunaldi(Zenbakia),
    FOREIGN KEY (EboluzioaID) REFERENCES Pokemon_Pokedex(PokemonID)
);

CREATE TABLE IF NOT EXISTS Pokemon_Pokedex_Mota (
    PokemonID INTEGER NOT NULL,
    MotaIzena TEXT NOT NULL,
    PRIMARY KEY (PokemonID, MotaIzena),
    FOREIGN KEY (PokemonID) REFERENCES Pokemon_Pokedex(PokemonID) ON DELETE CASCADE,
    FOREIGN KEY (MotaIzena) REFERENCES Mota(Izena) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS Indartsu_DA(
    MotaIndartsua TEXT NOT NULL,
    MotaAhula TEXT NOT NULL,
    PRIMARY KEY (MotaIndartsua, MotaAhula),
    FOREIGN KEY (MotaIndartsua) REFERENCES Mota(Izena) ON DELETE CASCADE,
    FOREIGN KEY (MotaAhula) REFERENCES Mota(Izena) ON DELETE CASCADE
);

-- ============================================================
-- 4. Tabla de Usuarios (Erabiltzaile)
-- Según el documento, la clave principal es el DNI
-- ============================================================
CREATE TABLE IF NOT EXISTS Erabiltzaile (
    DNI TEXT PRIMARY KEY,            -- 'Bere gakoa DNI-a izango da'
    Izena TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Pasahitza TEXT NOT NULL,
    Bio TEXT,                        -- Biografía
    Sortze_Data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Rol TEXT,                        -- Rol del usuario (admin/user)
    
    -- El documento menciona que el usuario guarda un 'Pokemon_TaldeID'.
    -- Esto podría indicar un equipo principal o seleccionado.
    TaldeIzen Text,         
    
    -- Nota: Se añade la FK al final o se asume creación diferida para evitar ciclos
    
);

-- ============================================================
-- 5. Tabla de Equipo Pokémon (Pokemon_Talde)
-- Representa un Pokémon capturado/instanciado en el equipo de un usuario
-- ============================================================
CREATE TABLE IF NOT EXISTS Pokemon_Talde (
    TaldeIzen TEXT,
    Izena TEXT,                      -- Mote o nombre personalizado
    Estatistikak_Guztira INTEGER,    -- Suma total de estadísticas
    
    -- Relación 'Dauka': Vincula con la especie de la Pokédex
    Pokemon_PokedexPokemonID INTEGER NOT NULL PRIMARY KEY,
    
    -- Relación 'Harrapatu' (Capturar): Vincula con el Usuario (Dueño)
    -- El documento indica que se guarda el DNI del "Harraparia" (Cazador)

    FOREIGN KEY (Pokemon_PokedexPokemonID) REFERENCES Pokemon_Pokedex(PokemonID),
    FOREIGN KEY (TaldeIzen) REFERENCES Erabiltzaile(TaldeIzen) ON DELETE CASCADE,

);


-- ============================================================
-- 6. Tabla de Amigos (Lagunak / Laguna da)
-- Relación N:M entre usuarios
-- ============================================================
CREATE TABLE IF NOT EXISTS Lagunak (
    ErabiltzaileDNI1 TEXT NOT NULL,
    ErabiltzaileDNI2 TEXT NOT NULL,
    
    PRIMARY KEY (ErabiltzaileDNI1, ErabiltzaileDNI2),
    FOREIGN KEY (ErabiltzaileDNI1) REFERENCES Erabiltzaile(DNI) ON DELETE CASCADE,
    FOREIGN KEY (ErabiltzaileDNI2) REFERENCES Erabiltzaile(DNI) ON DELETE CASCADE
);

-- ============================================================
-- 8. Tabla de Capturas (Harrapatu)
-- Registra qué Pokémon ha capturado cada usuario
-- ============================================================
CREATE TABLE IF NOT EXISTS Harrapatu (
    ErabiltzaileDNI TEXT NOT NULL,
    PokemonID INTEGER NOT NULL,
    Harrapatu_Data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Fecha de captura
    PRIMARY KEY (ErabiltzaileDNI, PokemonID),  -- Un usuario puede capturar un Pokémon solo una vez
    FOREIGN KEY (ErabiltzaileDNI) REFERENCES Erabiltzaile(DNI) ON DELETE CASCADE,
    FOREIGN KEY (PokemonID) REFERENCES Pokemon_Pokedex(PokemonID) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS Mezua (
    ErabiltzaileDNI TEXT NOT NULL,
    Mezua TEXT NOT NULL,
    Data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ErabiltzaileDNI) REFERENCES Erabiltzaile(DNI) ON DELETE CASCADE,
    PRIMARY KEY (ErabiltzaileDNI, Data)
);



