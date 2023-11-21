import unittest

from card_wars.card import *
from card_wars.deck import Deck
from card_wars.import_cards import find_card, get_all_cards

# The purpose of this test is to assert all cards are correctly parsed from json sources.

# card_import_test.py removed, since this test also imports all cards


class TestDeck(unittest.TestCase):
    def test_deck(self):
        deck = Deck(name="My Big Deck", card_limit=None, copies_allowed=300)

        for card in get_all_cards():
            [deck.add_card(card) for _ in range(1)]

        for card in deck:
            print(card.name)
            self.assertIsInstance(card, Card)


if __name__ == "__main__":
    unittest.main()
