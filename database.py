import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name="biker.db"):
        self.db_name = db_name
        self.create_tables()   # belangrijk!

    # ----------------------------------------------------------
    # Database connectie
    # ----------------------------------------------------------
    def connect(self):
        return sqlite3.connect(self.db_name)

    # ----------------------------------------------------------
    # Tabellen aanmaken
    # ----------------------------------------------------------
    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        # ====== Reserveringen tabel ======
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                bike_type TEXT NOT NULL,
                accessories TEXT,
                comment TEXT,
                created_at TEXT NOT NULL
            )
        """)

        # ====== Schademeldingen tabel ======
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS damage_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                bike_type TEXT NOT NULL,
                damages TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        # ====== Medewerkers tabel ======
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # ====== DEMO-ACCOUNTS VEILIG TOEVOEGEN ======
        demo_accounts = [
            ("admin", "admin", "manager"),
            ("balie", "admin", "balie"),
            ("reparateur", "admin", "reparateur")
        ]

        for username, password, role in demo_accounts:
            cursor.execute("""
                INSERT OR IGNORE INTO employees (username, password, role)
                VALUES (?, ?, ?)
            """, (username, password, role))

        conn.commit()
        conn.close()

    # ----------------------------------------------------------
    # Reservering opslaan
    # ----------------------------------------------------------
    def save_reservation(self, name, email, start_date, end_date, bike_type, accessories, comment):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO reservations (
                name, email, start_date, end_date, bike_type, accessories, comment, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
                           name,
                           email,
                           start_date,
                           end_date,
                           bike_type,
                           accessories,
                           comment,
                           datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

    # ----------------------------------------------------------
    # Schade melden opslaan
    # ----------------------------------------------------------
    def save_damage_report(self, name, email, bike_type, damages):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO damage_reports (
                name, email, bike_type, damages, created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            bike_type,
            damages,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

    # ----------------------------------------------------------
    # Medewerker inloggen
    # ----------------------------------------------------------
    def login_employee(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, role
            FROM employees
            WHERE username = ? AND password = ?
        """, (username, password))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                "id": result[0],
                "username": result[1],
                "role": result[2]
            }

        return None
