import json

from card_wars import card
from card_wars.import_cards import read_cards_from

if __name__ == "__main__":
    cards = read_cards_from("data/card/minion/minions.json")
    cards.extend(read_cards_from("data/card/weapon/weapons.json"))
    cards.extend(read_cards_from("data/card/spell/spells.json"))

    for card in cards:
        print(card.card_id, card.name)
