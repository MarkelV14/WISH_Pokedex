#!/usr/bin/env python3
import sqlite3
import hashlib
import sys

def hash_password(password):
    salt = "mi_salt_secreto"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def create_admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Verificar si ya existe un admin
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if cursor.fetchone():
        print("🔴 Administratzailea dagoeneko existitzen da!")
        conn.close()
        return
    
    # Crear usuario admin
    password_hash = hash_password("admin123")
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, role, is_approved, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ('admin', 'admin@pokdex.com', password_hash, 'admin', 1, 1))
    
    conn.commit()
    conn.close()
    print("✅ Administratzailea sortu da!")
    print("Erabiltzailea: admin")
    print("Pasahitza: admin123")

if __name__ == '__main__':
    create_admin()
