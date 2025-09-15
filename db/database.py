import sqlite3
import json
from models.item import Item
from models.stuff import Stuff


class Database:
    def __init__(self, user_db="dofus.db", perfect_db="perfect_items.db"):
        self.user_db = user_db
        self.perfect_db = perfect_db
        self._init_db(user_db)
        self._init_db(perfect_db)

    def _init_db(self, db_path: str):
        """Crée la table items si elle n’existe pas déjà"""
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                categorie TEXT,
                level INTEGER,
                stats TEXT
            )
            """)
            conn.commit()

    # -----------------------------
    # Récupération des items
    # -----------------------------
    def get_items(self, perfect: bool = False):
        """Récupère les items de la base de données."""
        db_path = self.perfect_db if perfect else self.user_db
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, categorie, level, stats FROM items")
            rows = cursor.fetchall()
            return [
                (id_, Item(name, categorie, level, json.loads(stats)))
                for id_, name, categorie, level, stats in rows
            ]

    # -----------------------------
    # Ajout d’un item
    # -----------------------------
    def add_item(self, item: Item, perfect: bool = False):
        """Ajoute un item dans la DB utilisateur ou parfaite."""
        db_path = self.perfect_db if perfect else self.user_db
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items (name, categorie, level, stats) VALUES (?, ?, ?, ?)",
                (item.name, item.categorie, item.level, json.dumps(item.stats))
            )
            conn.commit()

    # -----------------------------
    # Suppression d’un item
    # -----------------------------
    def delete_item(self, item_id: int, perfect: bool = False, force: bool = False):
        """
        Supprime un item par ID.
        perfect: True = item parfait
        force: True = autoriser suppression même pour parfait
        """
        if perfect and not force:
            raise ValueError("Suppression interdite pour les items parfaits.")
        
        db_path = self.perfect_db if perfect else self.user_db
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
            conn.commit()

    # -----------------------------
    # Mise à jour d’un item utilisateur
    # -----------------------------
    def update_item(self, item_id: int, item: Item, perfect: bool = False):
        """Met à jour un item utilisateur (interdit pour la DB parfaite)."""
        if perfect:
            raise ValueError("Modification interdite dans la base des items parfaits.")

        with sqlite3.connect(self.user_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE items
                SET name = ?, categorie = ?, level = ?, stats = ?
                WHERE id = ?
                """,
                (item.name, item.categorie, item.level, json.dumps(item.stats), item_id)
            )
            conn.commit()
