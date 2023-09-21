from card_wars.card import *
from card_wars.deck import Deck
from card_wars.import_cards import find_card, get_all_cards, read_cards_from

if __name__ == "__main__":
    # Create deck instance
    deck = Deck(name="My Big Deck", card_limit=30)

    # Add two copies of all available cards
    for card in get_all_cards():
        [deck.add_card(card) for _ in range(2)]

    # Fill rest of deck with copies of same card
    deck.fill_with_card(find_card("Gnome"))

    deck.shuffle()

    # This method only returns the card and pops it from deck.
    # It doesn't add card to hand. Hand is handled in Board class.
    drawn_card = deck.draw_card()

    if drawn_card:
        print(f"Drawn Card: {drawn_card}")

    print(deck)

    deck2 = Deck("Deck 2")
    deck2.add_card(find_card("m00"))
    deck2.fill_with_card(find_card("s02"))

    print(deck2)
