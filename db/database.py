import sqlite3
import json
from models.item import Item
from models.stuff import Stuff

class Database:
    def __init__(self, user_db="dofus.db", perfect_db="perfect.db"):
        self.user_db = user_db
        self.perfect_db = perfect_db
        self.conn = sqlite3.connect(self.user_db)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            level INTEGER,
            stats TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stuffs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            items TEXT
        )
        """)
        self.conn.commit()

    # --- Items ---
    def add_item(self, item: Item, perfect=False):
        if perfect:
            raise ValueError("Impossible d’ajouter un item directement dans la DB des items parfaits.")
        with sqlite3.connect(self.user_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items (name, type, level, stats) VALUES (?, ?, ?, ?)",
                (item.name, item.type, item.level, json.dumps(item.stats))
            )
            conn.commit()


    def get_items(self, perfect=False):
        db_path = self.perfect_db if perfect else self.user_db
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, type, level, stats FROM items")
            rows = cursor.fetchall()
            return [(id_, Item(name, type_, level, json.loads(stats))) for id_, name, type_, level, stats in rows]
        
    def delete_item(self, item_id: int):
        with sqlite3.connect(self.user_db) as conn:
            # On ouvre une connexion à chaque requête pour éviter les problèmes de concurrence
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
            conn.commit()


    # --- Stuffs ---
    def add_stuff(self, stuff: Stuff):
        import json
        items = []
        with sqlite3.connect(self.user_db) as conn:
            cursor = conn.cursor()
            for items in stuff.items.values():
                for item in items:
                    cursor.execute(
                        "SELECT id FROM items WHERE name = ? AND type = ? AND level = ?",
                        (item.name, item.type, item.level)
                    )
                    res = cursor.fetchone()
                    if res:
                        items.append(res[0])
            cursor.execute(
                "INSERT INTO stuffs (name, items) VALUES (?, ?)",
                (stuff.name, json.dumps(items))
            )
            conn.commit()

    def get_stuffs(self):
        import json
        with sqlite3.connect(self.user_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, items FROM stuffs")
            rows = cursor.fetchall()
            return [(id_, name, json.loads(items)) for id_, name, items in rows]


    def delete_stuff(self, stuff_id: int):
        with sqlite3.connect(self.user_db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM stuffs WHERE id = ?", (stuff_id,))
            conn.commit()

