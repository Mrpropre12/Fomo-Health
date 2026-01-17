import sqlite3
import os

DB_PATH = 'database/fomo_health.db'

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table clinique
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clinic_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            hours TEXT
        )
    ''')
    
    # Données réelles
    data = [
        ("Clinique Fomo Health Saguenay", "123 Rue de l'Hôpital, Saguenay QC G7H 1A1", "Nous sommes ouvert du lundi à vendre de 8h à 16h et le samedi de 9h à 15h"),
        ("Urgences Cardio-Chicoutimi", "456 Av. de la Santé, Chicoutimi QC", "24h/24 7j/7")
    ]
    cursor.executemany('INSERT OR REPLACE INTO clinic_info (name, address, hours) VALUES (?, ?, ?)', data)
    
    conn.commit()
    conn.close()
    print(f"✅ DB: {DB_PATH}")
    print("Vérif: SELECT * FROM clinic_info;")

if __name__ == "__main__":
    init_db()
