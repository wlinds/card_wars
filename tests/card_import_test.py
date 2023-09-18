import json

from src.card_wars import card


def read_minion_cards_from(json_file_path):
    card_list = []

    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            for card_data in data:
                if card_data.get("card_type") == "minion":
                    minion_card = card.Minion(
                        name=card_data["name"],
                        description=card_data["description"],
                        mana_cost=card_data["mana_cost"],
                        attack=card_data["attack"],
                        health=card_data["health"],
                        race=card_data.get("race"),
                        ability=card_data.get("ability"),
                    )
                    card_list.append(minion_card)

    except FileNotFoundError:
        print(f"File not found: {json_file_path}")

    return card_list


if __name__ == "__main__":
    minion_cards = read_minion_cards_from("data/card/minion/minions.json")

    for card in minion_cards:
        print(card)

    print("hi")
