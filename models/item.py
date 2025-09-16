from typing import List, Dict, Optional
class Item:
    def __init__(self, name: str, categorie: str, level: int, stats: Dict[str, Optional[int]]):
        self._name = name
        self._categorie = categorie
        self._level = level
        self._stats = stats

    def __repr__(self):
        return f"{self.name} ({self.categorie}, lvl {self.level}) - {self.stats}"

    @property
    def name(self) -> str:
        return self._name
    @property
    def categorie(self) -> str:
        return self._categorie
    @property
    def level(self) -> int:
        return self._level
    @property
    def stats(self) -> Dict[str, int]:
        return self._stats
    
    @stats.setter
    def stats(self, new_stats: Dict[str, int]):
        self._stats = new_stats
    @name.setter
    def name(self, new_name: str):
        self._name = new_name
    @categorie.setter
    def categorie(self, new_categorie: str):
        self._categorie = new_categorie
    @level.setter
    def level(self, new_level: int):
        self._level = new_level
    