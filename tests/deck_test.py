from src.card_wars.card import *
from src.card_wars.deck import Deck
from src.card_wars.import_cards import read_cards_from

if __name__ == "__main__":
    # Create deck instance
    deck = Deck(name="My Big Deck", card_limit=30)

    # Dict for json files
    json_files = [
        "data/card/minion/minions.json",
        "data/card/weapon/weapons.json",
        "data/card/spell/spells.json",
    ]

    # Read dict, add one of each card to deck
    for json_file in json_files:
        cards = read_cards_from(json_file)
        for card in cards:
            deck.add_card(card)

    # Fill rest of deck with copies of same card
    deck.fill_with_card(
        Minion("Goblin", "A small creature with a funky smell.", 1, 2, 2, "Goblin")
    )

    print(deck)

    deck.shuffle()
    drawn_card = deck.draw_card()

    if drawn_card:
        print(f"Drawn Card: {drawn_card}")

    print(deck)

    for i in range(len(deck.cards) + 1):
        drawn_card = deck.draw_card()
        if drawn_card:
            print(f"Drawn Card: {drawn_card}")

        print(deck)
