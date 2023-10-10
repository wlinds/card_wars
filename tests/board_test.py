import unittest

from card_wars.board import Board
from card_wars.deck import get_test_deck


class TestBoard(unittest.TestCase):
    def test_add_to_field(self):
        board = Board()
        goblin_deck = get_test_deck("goblin")
        goblin_card = goblin_deck.get_card(0)

        board.add_to_field(goblin_card, 1)
        board.add_to_field(goblin_card, 2)

        # Check if board contains one goblin card on each side
        for player_field in [board.p1_field, board.p2_field]:
            for minion in player_field:
                self.assertEqual(minion.race, "Goblin")

        # Adding non-minion card to the field, should be invalid
        with self.assertRaises(ValueError):
            board.add_to_field("Not a goblin.", 2)


if __name__ == "__main__":
    unittest.main()
