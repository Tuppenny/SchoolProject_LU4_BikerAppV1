import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name="biker.db"):
        self.db_name = db_name
        self.create_tables()

    # ==== database connectie ====
    def connect(self):
        return sqlite3.connect(self.db_name)

    # ==== tabellen aanmaken ====
    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        # ==== reserveringen tabe (AI gemaakt) (Template) ====
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
                total_price REAL,
                borg REAL,
                status TEXT DEFAULT 'open',
                return_date TEXT,
                borg_status TEXT DEFAULT 'open',
                created_at TEXT NOT NULL
            )
        """)

        # ==== schademeldingen tabel ====
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS damage_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                bike_type TEXT,
                damages TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'wacht'
            )
        """)

        # ==== medewerkers tabel ====
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # ==== demo accounts toevoegen ====
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

    # ==== reservering opslaan ====
    def save_reservation(self, name, email, start_date, end_date, bike_type,
                         accessories, comment, total_price, borg):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO reservations (
                name, email, start_date, end_date, bike_type,
                accessories, comment, total_price, borg,
                status, return_date, borg_status, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'open', NULL, 'open', ?)
        """, (
            name,
            email,
            start_date,
            end_date,
            bike_type,
            accessories,
            comment,
            total_price,
            borg,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

    # ==== reservering verwijderen ====
    def delete_reservation(self, reservation_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
        conn.commit()
        conn.close()

    # ==== 1 reservering ophalen (zonder borg_status) (AI gemaakt) ====
    # deze wordt gebruikt in de details-popup en verwacht 12 velden
    def get_reservation(self, reservation_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, email, start_date, end_date,
                   bike_type, accessories, comment,
                   total_price, borg, status, return_date
            FROM reservations
            WHERE id = ?
        """, (reservation_id,))

        row = cursor.fetchone()
        conn.close()
        return row

    # ==== reserveringen zoeken (inclusief borg_status) ====
    def search_reservations(self, keyword):
        conn = self.connect()
        cursor = conn.cursor()

        keyword = f"%{keyword}%"
        cursor.execute("""
            SELECT id, name, email, start_date, end_date,
                   bike_type, accessories, comment,
                   total_price, borg, status, return_date, borg_status
            FROM reservations
            WHERE name LIKE ?
               OR email LIKE ?
            ORDER BY created_at DESC
        """, (keyword, keyword))

        rows = cursor.fetchall()
        conn.close()
        return rows

    # ==== alle reserveringen ophalen (inclusief borg_status) ====
    def get_all_reservations(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, email, start_date, end_date,
                   bike_type, accessories, comment,
                   total_price, borg, status, return_date, borg_status
            FROM reservations
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows

    # ==== reservering status bijwerken ====
    def update_reservation_status(self, reservation_id, new_status):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE reservations
            SET status = ?
            WHERE id = ?
        """, (new_status, reservation_id))

        conn.commit()
        conn.close()

    # ==== reservering afronden met teruggave datum ====
    def complete_reservation(self, reservation_id, return_date):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE reservations
            SET status = 'afgerond', return_date = ?
            WHERE id = ?
        """, (return_date, reservation_id))

        conn.commit()
        conn.close()

    # ==== borg status wijzigen ====
    def update_borg_status(self, reservation_id, new_status):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE reservations
            SET borg_status = ?
            WHERE id = ?
        """, (new_status, reservation_id))

        conn.commit()
        conn.close()

    # ==== schade melden opslaan ====
    def add_damage_report(self, name, email, bike_type, damages):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO damage_reports (name, email, bike_type, damages, status)
            VALUES (?, ?, ?, ?, 'wacht')
        """, (name, email, bike_type, damages))

        conn.commit()
        conn.close()

    # ==== medewerker inloggen ====
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

    # ==== alle schade meldingen ophalen ====
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

    # ==== 1 schade melding ophalen ====
    def get_damage_report(self, report_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, email, bike_type, damages, created_at, status
            FROM damage_reports
            WHERE id = ?
        """, (report_id,))

        row = cursor.fetchone()
        conn.close()
        return row

    # ==== schade melding verwijderen ====
    def delete_damage_report(self, report_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM damage_reports WHERE id = ?", (report_id,))
        conn.commit()
        conn.close()

    # ==== schade meldingen zoeken ====
    def search_damage_reports(self, keyword):
        conn = self.connect()
        cursor = conn.cursor()

        keyword = f"%{keyword}%"
        cursor.execute("""
            SELECT id, name, email, bike_type, damages, created_at, status
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

    # ==== schade status wijzigen ====
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

    # ==== reparaties ophalen ====
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
