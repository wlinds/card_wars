from card_wars import logs
from card_wars.board import Board
from card_wars.deck import Deck, get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


@logs.game_state
def main():
    p1 = Player(name="P1 OSS", deck=Deck())
    p2 = Player(name="P2 OSR", deck=Deck())

    p1.deck.fill_with_card("msli000")
    p2.deck.fill_with_card("mbea000")

    cw = GameSession(p1, p2, Board())

    cw.draw_starting_cards(9)

    cw.end_turn()

    cw.player1.active_mana = 100
    cw.player2.active_mana = 100

    cw.player1.add_to_hand(find_card("mneu000"))
    cw.player2.add_to_hand(find_card("mneu000"))

    print(cw.player1.hand[-1])
    cw.play_card(1, -1)
    cw.play_card(1, 0, cw.board.p1_field[0])

    cw.player1.add_to_hand(find_card("mneu000"))
    cw.player2.add_to_hand(find_card("mneu000"))
    cw.play_card(1, -1)
    cw.play_card(1, -1)

    cw.play_card(1, 0, cw.board.p1_field[1])

    print(f"field={cw.board.p1_field[0]}")
    print(cw.board)


if __name__ == "__main__":
    main()
