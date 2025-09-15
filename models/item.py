class Item:
    def __init__(self, name: str, type_: str, level: int, stats: dict):
        self.name = name
        self.type = type_
        self.level = level
        self.stats = stats

    def __repr__(self):
        return f"{self.name} ({self.type}, lvl {self.level}) - {self.stats}"
