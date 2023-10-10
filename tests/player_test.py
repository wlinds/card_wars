import unittest

from card_wars import logs
from card_wars.deck import Deck, get_test_deck
from card_wars.import_cards import find_card
from card_wars.player import Player


class TestPlayerConstructor(unittest.TestCase):
    @logs.game_state
    def test_player(self):
        p1 = Player(name="Xx_ Dragonlord _xX", deck=get_test_deck("random"))
        p2 = Player(name="Bobby", deck=Deck())
        p3 = Player()

        p2.deck.fill_with_card(find_card("Goblin"))

        self.assertEqual(len(p1.deck), p1.deck.card_limit)

        p1.update_active_mana(10)
        self.assertEqual(p1.active_mana, 10)

        p2.take_damage(1)
        self.assertEqual(p2.health, p2.max_health - 1)


if __name__ == "__main__":
    unittest.main()
