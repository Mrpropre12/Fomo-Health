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
    #Création de la table des docteurs 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            speciality TEXT NULL
        )
    ''')
    # Création de la table pour les connaissances de l'IA (RAG)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clinic_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword_trigger TEXT NOT NULL,
            info_content TEXT NOT NULL
        )
    ''')
    
    # Données réelles
    data = [
        ("Clinique Fomo Health Saguenay", "123 Rue de l'Hôpital, Saguenay QC G7H 1A1", "Nous sommes ouverts du lundi au vendredi de 8 h à 16 h et le samedi de 9 h à 15 h"),
        ("Urgences Cardio-Chicoutimi", "456 Av. de la Santé, Chicoutimi QC", "24h/24 7j/7")
    ]
    cursor.executemany('INSERT OR REPLACE INTO clinic_info (name, address, hours) VALUES (?, ?, ?)', data)
    
    data = [
        ('parking', 'Le parking de la clinique est situé à l\'arrière du bâtiment, l\'entrée se fait par la rue latérale.'),
        ('prix', 'Les frais de consultation de base sont de 50 dollars, remboursables par la plupart des assurances.'),
        ('adresse', 'Fomo-Health est située au 123 boulevard de la Santé, bureau 400.'),
        ('urgence', 'En cas d\'urgence vitale, ne restez pas en ligne et composez immédiatement le 911.')
    ]
    cursor.executemany('INSERT INTO clinic_services (keyword_trigger, info_content) VALUES (?, ?)', data)
    
    data = [
        ("Dr.Smith", "Pediatre"),
        ("Dr.simon", "Généraliste")
    ]
    cursor.executemany('INSERT INTO doctors (name, speciality) VALUES (?, ?)', data)
    
    conn.commit()
    conn.close()
    print(f"✅ DB: {DB_PATH}")
    print("Vérif: SELECT * FROM clinic_info;")
    print("Table 'clinic_services' mise à jour avec succès.")
    print("table de docteur mise a jour ")

if __name__ == "__main__":
    init_db()
