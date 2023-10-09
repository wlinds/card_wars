import json

from card_wars.card import Minion, Spell, Weapon


def read_cards_from(json_file_path):
    card_list = []

    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            for card_data in data:
                if "card_text" in card_data:
                    card_text = card_data["card_text"]
                else:
                    card_text = ""

                if card_data.get("card_type") == "minion":
                    # Convert "buffs" to a list if it exists, or use an empty list by default
                    buffs = card_data.get("buffs", [])
                    minion_card = Minion(
                        card_id=card_data["card_id"],
                        name=card_data["name"],
                        description=card_data["description"],
                        card_text=card_text,
                        mana_cost=card_data["mana_cost"],
                        attack=card_data["attack"],
                        health=card_data["health"],
                        race=card_data.get("race"),
                        ability=card_data.get("ability"),
                        buffs=buffs,
                    )
                    card_list.append(minion_card)

                if card_data.get("card_type") == "weapon":
                    weapon_card = Weapon(
                        card_id=card_data["card_id"],
                        name=card_data["name"],
                        description=card_data["description"],
                        card_text=card_text,
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
                        card_text=card_text,
                        mana_cost=card_data["mana_cost"],
                        spell_type=card_data["spell_type"],
                        target=card_data["target"],
                        damage=card_data["damage"],
                    )
                    card_list.append(spell_card)

    except FileNotFoundError:
        print(f"File not found: {json_file_path}")

    return card_list


def find_card(card_id=None, minion_race=None):
    """
    Find card by search term (card_id) or card_name
    TODO: searching for card_name needs improvements (implement spell check, ignore capital letters etc)
    """
    cards = get_all_cards()

    if card_id:
        for card in cards:
            if card.card_id == card_id or card.name == card_id:
                return card

    if minion_race:
        return [card for card in cards if isinstance(card, Minion) and card.race == minion_race]

    print(f"Error: {card_id=} not found. Check import_cards and path.")
    return


def get_all_cards() -> list:
    """
    Return a list of card objects
    """
    cards = read_cards_from("data/card/minion/minions.json")
    cards.extend(read_cards_from("data/card/weapon/weapons.json"))
    cards.extend(read_cards_from("data/card/spell/spells.json"))

    return cards


if __name__ == "__main__":
    search_by_id = find_card("mgno001")
    print(search_by_id)
    print(type(search_by_id))

    search_by_name = find_card("Goblin")
    print(search_by_name)

    _ = find_card(minion_race="Gnome")
    print(_)
