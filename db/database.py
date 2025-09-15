import sqlite3
import json
from models.item import Item
from models.stuff import Stuff

class Database:
    def __init__(self, db_path="dofus.db"):
        self.conn = sqlite3.connect(db_path)
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
    def add_item(self, item: Item):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO items (name, type, level, stats) VALUES (?, ?, ?, ?)",
                       (item.name, item.type, item.level, json.dumps(item.stats)))
        self.conn.commit()

    def get_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, type, level, stats FROM items")
        rows = cursor.fetchall()
        return [(id_, Item(name, type_, level, json.loads(stats))) for id_, name, type_, level, stats in rows]

    def delete_item(self, item_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        self.conn.commit()

    # --- Stuffs ---
    def add_stuff(self, stuff: Stuff):
        items_ids = []
        cursor = self.conn.cursor()
        for items in stuff.items.values():
            for item in items:
                cursor.execute("SELECT id FROM items WHERE name = ? AND type = ? AND level = ?",
                               (item.name, item.type, item.level))
                res = cursor.fetchone()
                if res:
                    items_ids.append(res[0])
        cursor.execute("INSERT INTO stuffs (name, items) VALUES (?, ?)",
                       (stuff.name, json.dumps(items_ids)))
        self.conn.commit()

    def get_stuffs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, items FROM stuffs")
        return cursor.fetchall()

    def delete_stuff(self, stuff_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM stuffs WHERE id = ?", (stuff_id,))
        self.conn.commit()
