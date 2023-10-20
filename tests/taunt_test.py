from card_wars import logs
from card_wars.board import Board
from card_wars.deck import Deck, get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


@logs.game_state
def taunt_test():
    p1 = Player(name="P1 OSS", deck=Deck())
    p2 = Player(name="P2 OSR", deck=Deck())

    p1.deck.fill_with_card("mbea000")
    p2.deck.fill_with_card("mbea000")

    cw = GameSession(p1, p2, Board())

    cw.draw_starting_cards(10)

    cw.end_turn()

    cw.player1.active_mana = 10
    cw.player2.active_mana = 10

    for i in range(2):
        cw.play_card(1, 0, cw.player2)
        cw.play_card(2, 0, cw.player2)

    cw.add_to_hand(1, find_card("mneu000"))
    cw.add_to_hand(2, find_card("mneu000"))

    print(cw.player1_hand)
    cw.play_card(1, -1)
    cw.play_card(2, -1)

    cw.attack_phase()

    print(cw.board)


if __name__ == "__main__":
    taunt_test()
