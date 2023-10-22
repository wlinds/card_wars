from card_wars import logs
from card_wars.board import Board
from card_wars.deck import get_custom_deck, get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


@logs.game_state
def card_build_test():
    # Constructed deck, should iterate over all cards and test best combination to win
    p1 = Player(name="P1 Goblin Player", deck=get_test_deck("goblin"))

    # Classic deck for P1 to beat
    p2 = Player(name="P2 Classic Deck", deck=get_custom_deck("cccc"))

    # Shuffle both deck for random order
    p1.deck.shuffle()
    p2.deck.shuffle()

    # Create board instance
    board = Board()

    # Create game instance
    cw = GameSession(p1, p2, board)

    # Each player draws 3 staring cards
    cw.draw_starting_cards()

    # Call end_turn() to set active turn to 1 and mana for each player to 1.
    cw.end_turn()

    cards_to_play = []

    for i in range(len(cw.player2_hand)):
        print((cw.player2_hand[i].card_id))

    print(len(cw.player1_hand))

    # # While loop until one player wins
    # while p1.health > 0 and p2.health > 0:
    #     cw.draw_card(1)
    #     cw.draw_card(2)

    #     print(cw.player1_hand)

    #     # Try to play card at hand index[0] for each active mana
    #     for i in range(p1.active_mana):
    #         cw.play_card(1, 0)
    #     for i in range(p2.active_mana):
    #         cw.play_card(2, 0)

    #     print(cw)
    #     print(cw.board)
    #     cw.attack_phase()

    # print(cw)
    # print(cw.board)


if __name__ == "__main__":
    card_build_test()
