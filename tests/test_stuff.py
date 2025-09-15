from models.item import Item
from models.stuff import Stuff

def test_add_item_once():
    s = Stuff("Test Stuff")
    i = Item("Coiffe Bouftou", "coiffe", 20, {"Vitalité": 50})
    assert s.add_item(i)
    assert not s.add_item(i)  # doublon interdit
