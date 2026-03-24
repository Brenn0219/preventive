import sqlite3
import os


class Database:
    def __init__(self, filename: str = "database.db"):
        self.db_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.db_dir, filename)

    def initialize(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS assignees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location_id INTEGER NOT NULL,
                assignee_id INTEGER NOT NULL,

                FOREIGN KEY(location_id) REFERENCES locations(id) ON DELETE CASCADE,
                FOREIGN KEY(assignee_id) REFERENCES assignees(id)
            );
        """)

        conn.commit()
        conn.close()

    def get_connection(self):
        return sqlite3.connect(self.db_path)