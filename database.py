import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name="biker.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

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

        conn.commit()
        conn.close()

    # ---------- Reservering opslaan ----------
    def save_reservation(self, name, email, start, end, bike_type, accessories, comment):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO reservations (
                name, email, start_date, end_date, bike_type, accessories, comment, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            start,
            end,
            bike_type,
            accessories,
            comment,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

    # ---------- Reserveringen ophalen (voor later) ----------
    def get_all_reservations(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM reservations ORDER BY created_at DESC")
        data = cursor.fetchall()

        conn.close()
        return data
