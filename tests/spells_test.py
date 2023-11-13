from card_wars import logs
from card_wars.board import Board
from card_wars.deck import Deck, get_test_deck
from card_wars.game import GameSession
from card_wars.import_cards import find_card
from card_wars.player import Player


@logs.game_state
def main():
    p1 = Player(name="P1", deck=Deck())
    p2 = Player(name="P2", deck=Deck())

    p1.deck.fill_with_card("sneu000")
    p2.deck.fill_with_card("sneu000")
    cw = GameSession(p1, p2, Board())

    cw.start_game()

    cw.player1.active_mana = 100
    cw.player2.active_mana = 100

    cw.play_card(1, 0)
    cw.play_card(1, 0)

    print(cw)


if __name__ == "__main__":
    main()
