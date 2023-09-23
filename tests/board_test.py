from card_wars.board import Board
from card_wars.deck import get_test_deck

if __name__ == "__main__":
    board = Board()
    goblin_deck = get_test_deck("goblin")
    goblin_card = goblin_deck.get_card(0)
    board.add_to_field(goblin_card, 1)
    board.add_to_field(goblin_card, 2)
    print(board)

    board.add_to_field("Not a goblin.", 2)  # Should be invalid
