import unittest

from card_wars import logs
from card_wars.board import Board
from card_wars.deck import Deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card, get_all_cards
from card_wars.player import Player


class TestAllMinion(unittest.TestCase):
    def test_all_cards(self):
        p1 = Player(name="P1 ALL", deck=Deck(), max_hand_size=999)
        p2 = Player(name="P2 ALL", deck=Deck(), max_hand_size=999)

        board = Board()
        board.max_field_minion = 999

        all_minions = get_all_cards(minions=True, weapons=True, spells=True)

        for minion in all_minions:
            p1.deck.add_card(minion)
            p2.deck.add_card(minion)

        cw = GameSession(p1, p2, board)

        for i in range(len(p1.deck) + 1):
            p1.draw_card()
            cw.play_card(1, 0)
            cw.play_card(1, 0)
            p2.draw_card()
            cw.play_card(2, 0)
            cw.play_card(2, 0)

        print(cw)
        print(cw.board)

        while len(cw.board.p1_field) > 0:
            for minion in cw.board.p1_field:
                minion.take_damage(1)
                cw.remove_dead_minions(1)
                cw.player1.active_mana = 9999

        while len(cw.board.p2_field) > 0:
            for minion in cw.board.p2_field:
                minion.take_damage(1)
                cw.remove_dead_minions(2)
                cw.player2.active_mana = 9999

        print(cw)
        print(cw.board)
        print(p2.get_hand())

        while len(p2.hand) > 0 and len(p1.hand) > 0:
            p1.draw_card()
            p2.draw_card()
            cw.player2.active_mana = 9999
            cw.player1.active_mana = 9999
            cw.play_card(1, 0)
            cw.play_card(1, -1)
            cw.play_card(2, 0)
            cw.play_card(2, -1)
            cw.remove_dead_minions(1)
            cw.remove_dead_minions(2)

        print(cw)
        print(cw.board)


if __name__ == "__main__":
    unittest.main()
