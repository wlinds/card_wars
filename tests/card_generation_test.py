from card_wars import logs
from card_wars.board import Board
from card_wars.deck import Deck, get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


@logs.game_state
def goblin_vs_gnomes_test():
    p1 = Player(name="P1 OSS", deck=Deck())
    p2 = Player(name="P2 OSR", deck=Deck())

    p1.deck.fill_with_card("mgnome004")
    p2.deck.fill_with_card("mgob006")

    cw = GameSession(p1, p2, Board())

    cw.draw_starting_cards()

    cw.end_turn()

    cw.player1.active_mana = 12
    cw.player2.active_mana = 12

    for i in range(5):
        cw.play_card(1, 0, cw.player2)
        cw.play_card(2, 0, cw.player2)

    print(cw)
    print(cw.board)
    for minion in cw.player1.hand:
        print(minion.name)
    for minion in cw.player2.hand:
        print(minion.name)


if __name__ == "__main__":
    goblin_vs_gnomes_test()
