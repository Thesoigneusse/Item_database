from models.item import Item
from models.stuff import Stuff
from db.database import Database
import json

STATS_CATEGORIES = {
    "Effets principaux": ["Vitalité", "Force", "Intelligence", "Chance", "Agilité", "Sagesse", "PA", "PM", "Portée"],
    "Effets secondaires": ["Initiative", "Prospection", "Invocation", "Tacle", "Fuite", "Soins", "Critiques"],
    "Dommages": ["Puissance", "Dommages Neutre", "Dommages Terre", "Dommages Feu", "Dommages Eau", "Dommages Air"],
    "Résistances": [
        "Résistance Neutre", "Résistance Terre", "Résistance Feu", "Résistance Eau", "Résistance Air",
        "% Résistance Neutre", "% Résistance Terre", "% Résistance Feu", "% Résistance Eau", "% Résistance Air",
        "Esquive PA", "Esquive PM", "Retrait PA", "Retrait PM"
    ]
}

def choisir_stats():
    stats = {}
    while True:
        print("\n--- Catégories de caractéristiques ---")
        categories = list(STATS_CATEGORIES.keys())
        for i, cat in enumerate(categories, start=1):
            print(f"{i}. {cat}")
        choix_cat = input("Numéro de la catégorie (ENTER pour finir): ")
        if not choix_cat:
            break
        try:
            idx_cat = int(choix_cat) - 1
            cat_name = categories[idx_cat]
            stats_list = STATS_CATEGORIES[cat_name]
            for j, stat in enumerate(stats_list, start=1):
                print(f"{j}. {stat}")
            choix_stat = input("Numéro de la stat: ")
            if not choix_stat:
                continue
            stat = stats_list[int(choix_stat) - 1]
            val = int(input(f"Valeur de {stat}: "))
            stats[stat] = val
        except (ValueError, IndexError):
            print("⚠ Entrée invalide.")
    return stats


def menu():
    db = Database()
    while True:
        print("\n=== Menu Principal ===")
        print("1. Ajouter un item")
        print("2. Lister les items")
        print("3. Supprimer un item")
        print("4. Créer un stuff")
        print("5. Lister les stuffs")
        print("6. Supprimer un stuff")
        print("7. Quitter")

        choix = input("Choix: ")
        if choix == "1":
            name = input("Nom de l'item: ")
            categorie = input("categorie (anneau, ceinture, cape, coiffe, etc.): ").lower()
            level = int(input("Niveau: "))
            stats = choisir_stats()
            item = Item(name, categorie, level, stats)
            db.add_item(item)

        elif choix == "2":
            for id_, item in db.get_items():
                print(f"{id_}: {item}")

        elif choix == "3":
            for id_, item in db.get_items():
                print(f"{id_}: {item}")
            choix_id = int(input("ID de l'item à supprimer: "))
            db.delete_item(choix_id)

        elif choix == "4":
            name = input("Nom du stuff: ")
            stuff = Stuff(name)
            for id_, item in db.get_items():
                print(f"{id_}: {item}")
            choix_id = int(input("ID de l'item à ajouter (ENTER pour finir): ") or -1)
            if choix_id != -1:
                for id_, item in db.get_items():
                    if id_ == choix_id:
                        stuff.add_item(item)
            db.add_stuff(stuff)

        elif choix == "5":
            for id_, name, items in db.get_stuffs():
                print(f"{id_}: {name} ({items})")

        elif choix == "6":
            for id_, name, items in db.get_stuffs():
                print(f"{id_}: {name}")
            choix_id = int(input("ID du stuff à supprimer: "))
            db.delete_stuff(choix_id)

        elif choix == "7":
            break
