import unittest

from card_wars import logs
from card_wars.board import Board
from card_wars.deck import Deck, get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


class TestHealthShare(unittest.TestCase):
    def test_health_share(self):
        p1 = Player(name="P1 OSS", deck=Deck())
        p2 = Player(name="P2 OSR", deck=Deck())

        p1.deck.fill_with_card("mdem001")
        p2.deck.fill_with_card("mdem001")

        cw = GameSession(p1, p2, Board())

        cw.draw_starting_cards(10)

        cw.end_turn()

        cw.player1.active_mana = 10
        cw.player2.active_mana = 10

        for i in range(5):
            cw.play_card(1, 0, cw.player2)
            cw.play_card(2, 0, cw.player2)

        print("yy")
        print(cw.board)
        cw.board.p1_field[0].attack = 10

        cw.attack_phase()
        cw.end_turn()

        print(cw)
        print(cw.board)


if __name__ == "__main__":
    unittest.main()
