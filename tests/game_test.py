from card_wars.board import Board
from card_wars.deck import get_test_deck
from card_wars.game import GameSession
from card_wars.player import Player


def goblin_vs_gnomes_test():
    p1 = Player(name="P1", deck=get_test_deck("goblin"))
    p2 = Player(name="P2", deck=get_test_deck("gnome"))

    board = Board(p1, p2)

    # Init GameSession with the board, player, decks and cards
    cw = GameSession(board)

    p1.deck.shuffle()
    p2.deck.shuffle()

    cw.draw_starting_cards()

    # Call end_turn() to set active turn to 1 and mana for each player to 1.
    cw.board.end_turn()

    print(cw.board)

    while p1.health > 0 and p2.health > 0:
        cw.board.draw_card(1)
        cw.board.draw_card(2)

        cw.board.draw_card(2)
        cw.board.draw_card(2)

        # Try to play card at hand index[0] for each active mana
        for i in range(p1.active_mana):
            cw.board.play_card(1, 0)
        for i in range(p2.active_mana):
            cw.board.play_card(2, 0)

        cw.board.attack_phase()
        print(cw.board)


if __name__ == "__main__":
    goblin_vs_gnomes_test()
