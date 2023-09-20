import json

from card_wars.card import Minion, Spell, Weapon


def read_cards_from(json_file_path):
    card_list = []

    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            for card_data in data:
                if card_data.get("card_type") == "minion":
                    minion_card = Minion(
                        card_id=card_data["card_id"],
                        name=card_data["name"],
                        description=card_data["description"],
                        mana_cost=card_data["mana_cost"],
                        attack=card_data["attack"],
                        health=card_data["health"],
                        race=card_data.get("race"),
                        ability=card_data.get("ability"),
                    )
                    card_list.append(minion_card)

                if card_data.get("card_type") == "weapon":
                    weapon_card = Weapon(
                        card_id=card_data["card_id"],
                        name=card_data["name"],
                        description=card_data["description"],
                        mana_cost=card_data["mana_cost"],
                        attack=card_data["attack"],
                        durability=card_data["durability"],
                    )
                    card_list.append(weapon_card)

                elif card_data.get("card_type") == "spell":
                    spell_card = Spell(
                        card_id=card_data["card_id"],
                        name=card_data["name"],
                        description=card_data["description"],
                        mana_cost=card_data["mana_cost"],
                        spell_type=card_data["spell_type"],
                        target=card_data["target"],
                        damage=card_data["damage"],
                    )
                    card_list.append(spell_card)

    except FileNotFoundError:
        print(f"File not found: {json_file_path}")

    return card_list
