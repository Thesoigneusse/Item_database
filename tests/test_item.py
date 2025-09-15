import pytest
from models.item import Item

def test_item_repr():
    item = Item("Coiffe Bouftou", "coiffe", 20, {"Vitalité": 50})
    assert "Coiffe Bouftou" in repr(item)
