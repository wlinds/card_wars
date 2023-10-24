import json

from card_wars.card import Minion, Spell, Weapon


def read_cards_from(path):
    card_list = []

    try:
        with open(path, "r") as file:
            data = json.load(file)
            for d in data:
                if "card_text" in d:
                    card_text = d["card_text"]
                else:
                    card_text = ""

                if d.get("card_type") == "minion":
                    # Get mechanics if it exists in data, else use empty list
                    battlecry = d.get("battlecry", [])
                    deathrattle = d.get("deathrattle", [])

                    base_stats = [d.get("attack", 1), d.get("health", 1), d.get("mana_cost", 0)]

                    minion_card = Minion(
                        card_id=d["card_id"],
                        name=d["name"],
                        base_stats=base_stats,
                        ability=d.get("ability"),
                        race=d.get("race"),
                        battlecry=battlecry,
                        deathrattle=deathrattle,
                        description=d["description"],
                        card_text=card_text,
                    )
                    card_list.append(minion_card)

                if d.get("card_type") == "weapon":
                    weapon_card = Weapon(
                        card_id=d["card_id"],
                        name=d["name"],
                        description=d["description"],
                        card_text=card_text,
                        mana_cost=d["mana_cost"],
                        attack=d["attack"],
                        durability=d["durability"],
                    )
                    card_list.append(weapon_card)

                elif d.get("card_type") == "spell":
                    spell_card = Spell(
                        card_id=d["card_id"],
                        name=d["name"],
                        description=d["description"],
                        card_text=card_text,
                        mana_cost=d["mana_cost"],
                        spell_type=d["spell_type"],
                        target=d["target"],
                        damage=d["damage"],
                    )
                    card_list.append(spell_card)

    except FileNotFoundError:
        print(f"File not found: {path}")

    return card_list


def find_card(card_id=None, minion_race=None):
    """
    Find card by search term (card_id) or card_name.
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


def get_all_cards(minions=True, weapons=True, spells=True) -> list:
    """
    Return a list of card objects
    """
    cards = []
    if minions:
        cards.extend(read_cards_from("data/card/minion/minions.json"))
        cards.extend(read_cards_from("data/card/minion/undeads.json"))
    if weapons:
        cards.extend(read_cards_from("data/card/weapon/weapons.json"))
    if spells:
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
