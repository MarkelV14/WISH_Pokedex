-- ============================================================
-- 1. USUARIOS (Coincide con user_model.py)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    is_approved INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bio TEXT,
    talde_izen TEXT
);

-- ============================================================
-- 2. SESIONES (Necesario para auth_model.py)
-- ============================================================
CREATE TABLE IF NOT EXISTS user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- 3. DATOS POKÉDEX
-- ============================================================
CREATE TABLE IF NOT EXISTS Belaunaldi (
    Zenbakia INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Mota (
    Izena TEXT UNIQUE NOT NULL PRIMARY KEY,
    Irudia TEXT
);

CREATE TABLE IF NOT EXISTS Pokemon_Pokedex (
    PokemonID INTEGER PRIMARY KEY,
    Izena TEXT UNIQUE NOT NULL,
    Altuera REAL,
    Pisua REAL,
    Irudia TEXT,
    PS INTEGER,
    Eraso INTEGER,
    Defentsa INTEGER,
    Defentsa_esp INTEGER,
    Abiadura INTEGER,
    BelaunaldiaZenbakia INTEGER,
    EboluzioaID INTEGER,
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

CREATE TABLE IF NOT EXISTS Indartsu_DA (
    MotaIndartsua TEXT NOT NULL,
    MotaAhula TEXT NOT NULL,
    PRIMARY KEY (MotaIndartsua, MotaAhula),
    FOREIGN KEY (MotaIndartsua) REFERENCES Mota(Izena) ON DELETE CASCADE,
    FOREIGN KEY (MotaAhula) REFERENCES Mota(Izena) ON DELETE CASCADE
);

-- ============================================================
-- 4. INTERACCIÓN USUARIO - POKÉMON
-- ============================================================
CREATE TABLE IF NOT EXISTS Pokemon_Talde (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    Pokemon_PokedexID INTEGER NOT NULL,
    Izena TEXT,
    Estatistikak_Guztira INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (Pokemon_PokedexID) REFERENCES Pokemon_Pokedex(PokemonID)
);



CREATE TABLE IF NOT EXISTS Harrapatu (
    user_id INTEGER NOT NULL,
    PokemonID INTEGER NOT NULL,
    Harrapatu_Data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, PokemonID),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (PokemonID) REFERENCES Pokemon_Pokedex(PokemonID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Mezua (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    Mezua TEXT NOT NULL,
    Data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Lagunak (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    friend_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (friend_id) REFERENCES users (id),
    UNIQUE(user_id, friend_id) -- Ezin diozu pertsona berdinari birritan jarraitu
);