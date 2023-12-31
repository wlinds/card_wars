import unittest

from card_wars import logs
from card_wars.board import Board
from card_wars.deck import get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


class TestGS(unittest.TestCase):
    def test_gs(self):
        p1 = Player(name="P1 Goblin Player", deck=get_test_deck("goblin"))
        p2 = Player(name="P2 Gnome Player", deck=get_test_deck("gnome"))
        board = Board()

        # Init GameSession with the board, player, decks and cards
        cw = GameSession(p1, p2, board)

        cw.shuffle_decks()
        cw.draw_starting_cards()

        # Call end_turn() to set active turn to 1 and mana for each player to 1.
        cw.end_turn()

        while p1.health[0] > 0 and p2.health[0] > 0:
            p1.draw_card()
            p2.draw_card()

            # Try to play card at hand index[0] for each active mana
            for i in range(p1.active_mana):
                cw.play_card(1, 0)
                cw.play_card(1, -1)
            for i in range(p2.active_mana):
                cw.play_card(2, 0)
                cw.play_card(2, -1)

            print(cw)
            print(cw.board)
            cw.attack_phase()

        print(cw)
        print(cw.board)


if __name__ == "__main__":
    unittest.main()
