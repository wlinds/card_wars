from card_wars import logs
from card_wars.board import Board
from card_wars.deck import Deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card, get_all_cards
from card_wars.player import Player


@logs.game_state
def main():
    p1 = Player(name="P1 ALL", deck=Deck(), max_hand_size=999)
    p2 = Player(name="P2 ALL", deck=Deck(), max_hand_size=999)

    board = Board()

    all_minions = get_all_cards(minions=True, weapons=0, spells=0)

    cw = GameSession(p1, p2, board)

    cw.player1.mana_bar = 999
    cw.end_turn()

    cw.player1.add_to_hand(find_card("mdem002"))

    cw.play_card(1, 0)

    print(cw)
    print(cw.board)

    cw.end_turn()

    print(cw)

    cw.player1.add_to_hand(find_card("sneu001"))
    cw.play_card(1, 0)

    print(cw)
    print(cw.board)


if __name__ == "__main__":
    main()
