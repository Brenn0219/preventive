class SectorsReadRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        conn = self.db.get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT s.name, l.name, a.name, s.tipo
            FROM sectors s
            JOIN locations l ON l.id = s.location_id
            JOIN assignees a ON a.id = s.assignee_id
        """)

        rows = cur.fetchall()
        conn.close()

        return [
            {"setor": row[0], "local": row[1], "atribuido": row[2], "tipo": row[3]}
            for row in rows
        ]