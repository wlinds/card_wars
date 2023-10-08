import unittest

from card_wars import logs
from card_wars.board import Board
from card_wars.deck import Deck, get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


class TestAOEBattlecry(unittest.TestCase):
    @logs.game_state
    def test_aoe(self):
        p1 = Player(name="Xx_Dragonlord_xX", deck=Deck())
        p2 = Player(name="Bobby", deck=Deck())

        p1.deck.burn_deck()
        p2.deck.burn_deck()

        board = Board()

        cw = GameSession(p1, p2, board)

        # Add 2 grandmas and 2 Gnomes to p2 field
        for i in range(2):
            cw.board.add_to_field(find_card("Grandma Gnome"), 2)
            cw.board.add_to_field(find_card("Gnome"), 2)

        # Add dragon to P1 hand, set mana
        cw.player1_hand.append(find_card("Dragonite"))
        cw.player1.active_mana = 16
        print(cw.player1_hand)
        print(len(cw.board))

        # Crush all goblins except divine shields
        cw.play_card(1, 0)

        cw.remove_dead_minions(2)

        print(len(cw.board))

        # add second dragon, play it to crush the rest of the grandmas (jesus)
        cw.player1_hand.append(find_card("Dragonite"))
        cw.play_card(1, 0)

        cw.remove_dead_minions(2)

        self.assertEqual(len(cw.board), 2)  # Should only be 2 dragons
        print(cw.board)


if __name__ == "__main__":
    unittest.main()
