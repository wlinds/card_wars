from dataclasses import dataclass, field
from typing import List

from card_wars.card import Card
from card_wars.deck import Deck, get_test_deck


@dataclass
class Board:
    player1_deck: Deck
    player2_deck: Deck
    player1_hand: List[Card] = field(default_factory=list)
    player2_hand: List[Card] = field(default_factory=list)
    player1_field: List[Card] = field(default_factory=list)
    player2_field: List[Card] = field(default_factory=list)

    def draw_card(self, player_num):
        """
        Draw a card from deck and add it to hand.
        player_num: 1 or 2 to indicate which player is drawing.
        """
        if player_num not in [1, 2]:
            print("Invalid player number. Use 1 or 2.")
            return

        player_deck = self.player1_deck if player_num == 1 else self.player2_deck
        player_hand = self.player1_hand if player_num == 1 else self.player2_hand

        if player_deck.cards:
            drawn_card = player_deck.draw_card()
            player_hand.append(drawn_card)
            print(
                f"Player {player_num} drew: {drawn_card.name} [{drawn_card.attack}/{drawn_card.health}] Mana: {drawn_card.mana_cost}"
            )
        else:
            print(f"Player {player_num} has no cards left in their deck.")

    def play_card(self, player_num, card_index):
        """
        Play a card from hand into playing field.
        player_num: 1 or 2 to indicate which player is playing.
        card_index: The index of the card in the player's hand to play.
        """
        if player_num not in [1, 2]:
            print("Invalid player number. Use 1 or 2.")
            return

        player_hand = self.player1_hand if player_num == 1 else self.player2_hand
        player_field = self.player1_field if player_num == 1 else self.player2_field

        if not (0 <= card_index < len(player_hand)):
            print("Invalid card index.")
            return

        card_to_play = player_hand[card_index]
        player_field.append(card_to_play)
        del player_hand[card_index]

        print(
            f"Player {player_num} played: {card_to_play.name} "
            f"[{card_to_play.attack}/{card_to_play.health}] Mana: {card_to_play.mana_cost}"
        )

    def __str__(self):
        board_str = "Board State:\n"
        board_str += f"Player 1 Deck: {len(self.player1_deck.cards)} cards\n"
        board_str += f"Player 2 Deck: {len(self.player2_deck.cards)} cards\n"
        board_str += f"Player 1 Hand: {len(self.player1_hand)} cards\n"
        board_str += f"Player 2 Hand: {len(self.player2_hand)} cards\n"
        board_str += f"Player 1 Field: {len(self.player1_field)} cards\n"
        board_str += f"Player 2 Field: {len(self.player2_field)} cards\n"
        return board_str


if __name__ == "__main__":
    player1_deck = get_test_deck("goblin")
    player2_deck = get_test_deck("gnome")

    # Create a board with the two decks
    board = Board(player1_deck=player1_deck, player2_deck=player2_deck)

    # Each player draws 7 cards
    for i in range(7):
        board.draw_card(1)
        board.draw_card(2)

    # Each player plays their first drawn card:
    board.play_card(1, 0)
    board.play_card(2, 0)

    print(board)
