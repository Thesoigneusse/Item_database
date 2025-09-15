from .item import Item

class Stuff:
    def __init__(self, name: str):
        self.name = name
        self.items = {}

    def add_item(self, item: Item) -> bool:
        if item.categorie == "anneau":
            if len(self.items.get("anneau", [])) >= 2:
                return False
            self.items.setdefault("anneau", []).append(item)
        else:
            if item.categorie in self.items:
                return False
            self.items[item.categorie] = [item]
        return True

    def total_stats(self):
        totals = {}
        for items in self.items.values():
            for item in items:
                for stat, val in item.stats.items():
                    totals[stat] = totals.get(stat, 0) + val
        return totals

    def __repr__(self):
        lines = []
        for categorie, items in self.items.items():
            for item in items:
                lines.append(f"- {item}")
        return "\n".join(lines)
