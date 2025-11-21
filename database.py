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
                       CREATE TABLE IF NOT EXISTS damage_reports
                       (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT,
                           email TEXT,
                           bike_type TEXT,
                           damages TEXT,
                           created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                           status TEXT DEFAULT 'wacht'
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
    # Verwijder reservering
    # ----------------------------------------------------------
    def delete_reservation(self, reservation_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
        conn.commit()
        conn.close()

    # ----------------------------------------------------------
    # Reservering ophalen per ID
    # ----------------------------------------------------------
    def get_reservation(self, reservation_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT id,
                              name,
                              email,
                              start_date,
                              end_date,
                              bike_type,
                              accessories,
                              comment
                       FROM reservations
                       WHERE id = ?
                       """, (reservation_id,))

        row = cursor.fetchone()
        conn.close()
        return row

    # ----------------------------------------------------------
    # Reservering Zoeken op naam of email
    # ----------------------------------------------------------
    def search_reservations(self, keyword):
        conn = self.connect()
        cursor = conn.cursor()

        keyword = f"%{keyword}%"
        cursor.execute("""
                       SELECT id,
                              name,
                              email,
                              start_date,
                              end_date,
                              bike_type,
                              accessories,
                              comment
                       FROM reservations
                       WHERE name LIKE ?
                          OR email LIKE ?
                       ORDER BY created_at DESC
                       """, (keyword, keyword))

        rows = cursor.fetchall()
        conn.close()
        return rows

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

    # ----------------------------------------------------------
    # Reserveringen ophalen
    # ----------------------------------------------------------

    def get_all_reservations(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, email, start_date, end_date, bike_type, accessories, comment
            FROM reservations
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows

    # ----------------------------------------------------------
    # Alle Schade meldingen ophalen
    # ----------------------------------------------------------
    def get_all_damage_reports(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, email, bike_type, damages, created_at, status
            FROM damage_reports
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows

    # ----------------------------------------------------------
    # 1 Schade melding ophalen
    # ----------------------------------------------------------
    def get_damage_report(self, report_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT id, name, email, bike_type, damages, created_at
                       FROM damage_reports
                       WHERE id = ?
                       """, (report_id,))

        row = cursor.fetchone()
        conn.close()
        return row

    # ----------------------------------------------------------
    # Schade Melding verwijderen
    # ----------------------------------------------------------
    def delete_damage_report(self, report_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM damage_reports WHERE id = ?", (report_id,))
        conn.commit()
        conn.close()

    # ----------------------------------------------------------
    # Zoek Schademelding op naam email of schade
    # ----------------------------------------------------------
    def search_damage_reports(self, keyword):
        conn = self.connect()
        cursor = conn.cursor()

        keyword = f"%{keyword}%"
        cursor.execute("""
                       SELECT id, name, email, bike_type, damages, created_at
                       FROM damage_reports
                       WHERE name LIKE ?
                          OR email LIKE ?
                          OR bike_type LIKE ?
                          OR damages LIKE ?
                       ORDER BY created_at DESC
                       """, (keyword, keyword, keyword, keyword))

        rows = cursor.fetchall()
        conn.close()
        return rows

    # ----------------------------------------------------------
    # Schade status wijzigen
    # ----------------------------------------------------------
    def update_damage_status(self, report_id, new_status):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE damage_reports
                       SET status = ?
                       WHERE id = ?
                       """, (new_status, report_id))

        conn.commit()
        conn.close()

    # ----------------------------------------------------------
    # Reparaties ophalen
    # ----------------------------------------------------------
    def get_open_repairs(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT id, name, email, bike_type, damages, created_at, status
                       FROM damage_reports
                       WHERE status IN ('wacht', 'reparatie')
                       ORDER BY CASE status
                                    WHEN 'reparatie' THEN 0
                                    WHEN 'wacht' THEN 1
                                    END,
                                created_at DESC
                       """)

        rows = cursor.fetchall()
        conn.close()
        return rows
