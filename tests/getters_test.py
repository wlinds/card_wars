from card_wars import logs
from card_wars.board import Board
from card_wars.deck import get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


@logs.game_state
def main():
    p1 = Player(name="P1 Player")
    p2 = Player(name="P2 Player")

    board = Board()

    # Init GameSession with the board, player, decks and cards
    cw = GameSession(p1, p2, board)

    cw.player1.mana_bar = 20
    cw.player2.mana_bar = 20
    cw.end_turn()

    cw.player1.hand.append(find_card("mgno002"))
    cw.player1.hand.append(find_card("mgno002"))

    cw.play_card(1, 0)
    cw.play_card(1, 0)

    cw.player2.hand.append(find_card("mdra001"))
    cw.player2.hand.append(find_card("mdra001"))

    cw.play_card(2, 0)
    cw.play_card(2, 0)

    print(cw)
    print(board)

    cw.board.p2_field[0].take_damage(3)

    print(board)

    # HERE
    # When the second dragon dies and buff from it is removed,
    # the first dragon with only 2 hp also dies.
    # While this is intended, it might feel a bit unfair for the player.

    # To solve this, we either:
    # 1) cap the health reduction at 1 when a buff is removed
    # 2) Roll with it as intended game mechanic (not HS style) (see Stormwind Champion)

    cw.board.p2_field[1].take_damage(5)
    cw.remove_dead_minions(2)

    print(board)


if __name__ == "__main__":
    main()
