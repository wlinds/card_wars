import unittest

from card_wars.card import *
from card_wars.deck import Deck
from card_wars.import_cards import find_card, get_all_cards


class TestDeck(unittest.TestCase):
    def test_deck_operations(self):
        deck = Deck(name="My Big Deck", card_limit=300)

        # Add 1 copy of all cards
        for card in get_all_cards():
            [deck.add_card(card) for _ in range(1)]

        # Fill the deck up to 10% of deck with default Gnome
        deck.fill_with_card(find_card("Gnome"), fill=0.1)

        self.assertEqual(deck[-1].name, "Gnome")

        deck.shuffle()

        # This method only returns the card and pops it from deck.
        # It doesn't add card to hand. Hand is handled in Board class.
        drawn_card = deck.draw_card()

        if drawn_card:
            print(f"Drawn Card: {drawn_card}")

        deck2 = Deck("Deck 2")
        deck2.add_card(find_card("mgob000"))
        deck2.fill_with_card(find_card("snat000"))

        for _ in range(10):
            deck2.draw_card()

        self.assertEqual(len(deck2), 20)


if __name__ == "__main__":
    unittest.main()
