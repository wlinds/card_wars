import random

from card_wars import logs
from card_wars.board import Board
from card_wars.deck import get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


@logs.game_state
def goblin_vs_gnomes_test():
    p1 = Player(name="Gobb", deck=get_test_deck("goblin"))
    p2 = Player(name="Gnum", deck=get_test_deck("gnome"))

    board = Board()
    cw = GameSession(p1, p2, board)

    p1.deck.shuffle()
    p2.deck.shuffle()

    # Insert War Axe at second card in player 1 deck
    p1.deck.cards.insert(1, find_card("w000000"))

    cw.draw_starting_cards()

    print(cw)

    # Call end_turn() to set active turn to 1 and mana for each player to 1.
    cw.end_turn()

    while p1.health > 25 and p2.health > 25:
        cw.draw_card(1)
        # cw.draw_card(2)
        # cw.draw_card(2)
        # cw.draw_card(2)

        # Try to play card at hand index[0] for each active mana
        for i in range(p1.active_mana):
            cw.play_card(1, 0)
        for i in range(p2.active_mana):
            cw.play_card(2, 0)

        # Attack enemy minion with weapon if minion on board
        if p1.weapon and cw.board.p2_field:
            weapon_target = cw.board.p2_field[0]
            if p1.attack_with_weapon(target=weapon_target):
                cw.remove_dead_minions(2)

        # Else attack enemy player
        elif p1.weapon:
            weapon_target = cw.player2
            if p1.attack_with_weapon(target=weapon_target):
                print("This kills the player. Implement game ending logic here")  # TODO

        print(cw)
        print(cw.board)
        cw.attack_phase()

    print(cw)
    print(cw.board)


if __name__ == "__main__":
    goblin_vs_gnomes_test()
