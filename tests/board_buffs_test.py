import unittest

from card_wars import logs
from card_wars.board import Board
from card_wars.deck import Deck, get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


class TestBB(unittest.TestCase):
    def test_bb(self):
        p1 = Player(name="P1 OSS", deck=Deck())
        p2 = Player(name="P2 OSR", deck=Deck())

        p1.deck.fill_with_card("mdra001")
        p2.deck.fill_with_card("mdra001")

        cw = GameSession(p1, p2, Board())

        cw.draw_starting_cards(10)

        print(p1.hand[0])

        cw.end_turn()

        cw.player1.active_mana = 10
        cw.player2.active_mana = 10

        for i in range(5):
            cw.play_card(1, 0, cw.player2)
            cw.play_card(2, 0, cw.player2)

            print(cw)
            print(cw.board)

        cw.board.p1_field.pop(0, cw.board)
        cw.board.p1_field.pop(0, cw.board)
        cw.board.p1_field.pop(0, cw.board)

        print(cw)
        print(cw.board)
        print(cw.board.p1_field[0].mod_stats)
        print(cw.board.p2_field[0].mod_stats)

        cw.play_card(1, 0)

        print(cw.board.p1_field[0].mod_stats)
        print(cw.board.p2_field[0].mod_stats)


if __name__ == "__main__":
    unittest.main()
