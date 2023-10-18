from card_wars import logs
from card_wars.board import Board
from card_wars.deck import Deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card, get_all_cards
from card_wars.player import Player


@logs.game_state
def test_all_minion():
    p1 = Player(name="P1 ALL", deck=Deck(), max_hand_size=999)
    p2 = Player(name="P2 ALL", deck=Deck(), max_hand_size=999)

    board = Board()
    board.max_field_minion = 999

    all_minions = get_all_cards(minions=True, weapons=0, spells=0)

    for minion in all_minions:
        p1.deck.add_card(minion)
        p2.deck.add_card(minion)

    cw = GameSession(p1, p2, board)

    cw.player1.active_mana = 999
    cw.player2.active_mana = 999

    for i in range(len(p1.deck) + 1):
        cw.draw_card(1)
        cw.play_card(1, 0)
        cw.draw_card(2)
        cw.play_card(2, 0)

    print(cw)
    print(cw.board)

    while len(cw.board.p1_field) > 0:
        for minion in cw.board.p1_field:
            minion.take_damage(1)
            cw.remove_dead_minions(1)

    while len(cw.board.p2_field) > 0:
        for minion in cw.board.p2_field:
            minion.take_damage(1)
            cw.remove_dead_minions(2)

    print(cw)
    print(cw.board)


if __name__ == "__main__":
    test_all_minion()
