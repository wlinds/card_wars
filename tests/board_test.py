from card_wars.board import Board
from card_wars.card import Minion, Spell, Weapon
from card_wars.deck import Deck, get_test_deck
from card_wars.player import Player

if __name__ == "__main__":
    player1_deck = Deck("mana_storm")  # Create empty deck

    # Add one goblin, fill the rest of deck with Wild growth spell
    player1_deck.add_card(
        Minion("m00", "Goblin", "A small creature with a funky smell.", 1, 2, 2, "Goblin")
    )
    player1_deck.fill_with_card(
        Spell("s02", "Wild Growth", "Increases player mana by 2", 0, "nature", 4, 0)
    )

    player2_deck = get_test_deck("gnome")  # Get gnome deck for Player 2

    player1 = Player(deck=player1_deck)
    player2 = Player(deck=player2_deck)

    # Create a board with the two decks
    board = Board(player1, player2)

    # Each player draws 7 cards
    for i in range(7):
        board.draw_card(1)
        board.draw_card(2)

    # Player 1 plays 3 cards
    board.play_card(1, 0)
    board.play_card(1, 0)
    board.play_card(1, 0)

    # print(board)

    board.attack_phase()

    print(board)

    board.attack_phase()

    print(board)
