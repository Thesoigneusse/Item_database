import os
import tempfile
from db.database import Database
from models.item import Item

def test_add_and_get_item():
    db_path = tempfile.mktemp()
    db = Database(db_path)
    i = Item("Amulette Test", "amulette", 10, {"Chance": 5})
    db.add_item(i)
    items = db.get_items()
    assert any(item.name == "Amulette Test" for _, item in items)
    os.remove(db_path)
