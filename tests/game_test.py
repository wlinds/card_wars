from card_wars import logs
from card_wars.board import Board
from card_wars.deck import get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


@logs.game_state
def goblin_vs_gnomes_test():
    p1 = Player(name="P1 Goblin Player", deck=get_test_deck("goblin"))
    p2 = Player(name="P2 Gnome Player", deck=get_test_deck("gnome"))

    board = Board()

    # Init GameSession with the board, player, decks and cards
    cw = GameSession(p1, p2, board)

    for i in range(10):
        p1.deck.remove_card(i)
        p2.deck.remove_card(i)
        p1.deck.fill_with_card("sfro000")
        p2.deck.fill_with_card("sfro000")

    p1.deck.shuffle()
    p2.deck.shuffle()

    cw.draw_starting_cards()

    # Call end_turn() to set active turn to 1 and mana for each player to 1.
    cw.end_turn()

    while p1.health[0] > 0 and p2.health[0] > 0:
        cw.draw_card(1)
        cw.draw_card(2)

        # Try to play card at hand index[0] for each active mana
        for i in range(p1.active_mana):
            cw.play_card(1, 0)
        for i in range(p2.active_mana):
            cw.play_card(2, 0)

        print(cw)
        print(cw.board)
        cw.attack_phase()

    print(cw)
    print(cw.board)


if __name__ == "__main__":
    goblin_vs_gnomes_test()
