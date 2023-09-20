import random
from dataclasses import dataclass, field
from typing import List

from card_wars.card import Card, Minion, Spell, Weapon, cast_spell
from card_wars.deck import Deck, get_test_deck
from card_wars.player import Player


@dataclass
class Board:
    player1: Player
    player2: Player
    game_turn: int = 0
    player1_hand: List[Card] = field(default_factory=list)
    player2_hand: List[Card] = field(default_factory=list)
    player1_field: List[Card] = field(default_factory=list)
    player2_field: List[Card] = field(default_factory=list)
    player1_graveyard: List[Card] = field(default_factory=list)
    player2_graveyard: List[Card] = field(default_factory=list)

    def draw_card(self, player_num):
        """
        Draw a card from deck and add it to hand.
        player_num: 1 or 2 to indicate which player is drawing.
        """
        if player_num not in [1, 2]:
            print("Invalid player number. Use 1 or 2.")
            return

        player = self.player1 if player_num == 1 else self.player2
        player_hand = self.player1_hand if player_num == 1 else self.player2_hand

        if player.deck.cards:
            drawn_card = player.deck.draw_card()
            player_hand.append(drawn_card)

            if isinstance(drawn_card, Minion):
                print(
                    f"Player {player_num} drew: {drawn_card.name} [{drawn_card.attack}/{drawn_card.health}] Mana cost: {drawn_card.mana_cost}"
                )
            if isinstance(drawn_card, Spell or Weapon):
                print(
                    f"Player {player_num} drew: {drawn_card.name} Mana cost: {drawn_card.mana_cost}"
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

        player = self.player1 if player_num == 1 else self.player2
        player_hand = self.player1_hand if player_num == 1 else self.player2_hand
        player_field = self.player1_field if player_num == 1 else self.player2_field

        if not (0 <= card_index < len(player_hand)):
            print("Invalid card index.")
            return

        card_to_play = player_hand[card_index]

        # Check if player has enough active_mana to play card
        if player.active_mana >= card_to_play.mana_cost:
            if isinstance(card_to_play, Minion):
                player_field.append(card_to_play)
                del player_hand[card_index]

                # Deduct mana cost from active_mana
                player.active_mana -= card_to_play.mana_cost

                print(
                    f"[+] Player {player_num} played: {card_to_play.name} "
                    f"[{card_to_play.attack}/{card_to_play.health}] Mana: {card_to_play.mana_cost}"
                )
            elif isinstance(card_to_play, Spell):
                cast_spell(player, card_to_play.card_id)

            elif isinstance(card_to_play, Weapon):
                print("TODO: Implement equip weapon logic")
                pass
        else:
            print(f"Not enough mana to play {card_to_play.name}.")

    def attack_phase(self):
        """
        Simulate the attack phase where minions on the field can attack each other and deal damage.
        Handle minion deaths and player health deduction.
        """
        # Player 1 attacks Player 2's minions
        self.attack_player_minions(player_num=1, target_player_num=2)

        # Player 2 attacks Player 1's minions
        self.attack_player_minions(player_num=2, target_player_num=1)

        # Calculate total attack damage from remaining minions on the field
        player1_damage = sum(minion.attack for minion in self.player1_field)
        player2_damage = sum(minion.attack for minion in self.player2_field)

        # Deduct player health based on total attack damage
        self.player1.health -= player2_damage
        self.player2.health -= player1_damage

        # Check if either player has no minions left on the field
        if not self.player1_field:
            print("Player 1 has no minions left.")
            self.player2.health -= player1_damage  # Player 2's minions deal damage to Player 1
        if not self.player2_field:
            print("Player 2 has no minions left.")
            self.player1.health -= player2_damage  # Player 1's minions deal damage to Player 2

        self.game_turn += 1

        if self.player1.mana_bar < self.player1.max_mana_bar:
            self.player1.mana_bar += 1

        if self.player2.mana_bar < self.player2.max_mana_bar:
            self.player2.mana_bar += 1

        self.player1.update_active_mana()
        self.player2.update_active_mana()

    def attack_player_minions(self, player_num, target_player_num):
        """
        Simulate attacks from one player's minions to the other player's minions.
        """
        if player_num not in [1, 2] or target_player_num not in [1, 2]:
            print("Invalid player number. Use 1 or 2.")
            return

        player_field = self.player1_field if player_num == 1 else self.player2_field
        target_player_field = self.player1_field if target_player_num == 1 else self.player2_field

        for attacking_minion in player_field:
            if target_player_field:
                target_minion = random.choice(target_player_field)
                print(
                    f"[->] Player {player_num}'s {attacking_minion.name} "
                    f"[{attacking_minion.attack}/{attacking_minion.health}] "
                    f"attacks Player {target_player_num}'s {target_minion.name} "
                    f"[{target_minion.attack}/{target_minion.health}]"
                )
                # Calculate attack result
                attacking_minion.health -= target_minion.attack
                target_minion.health -= attacking_minion.attack

                self.remove_dead_minions(1)
                self.remove_dead_minions(2)

    def remove_dead_minions(self, player_num):
        """
        Remove dead minions (health <= 0) from the player's field.
        """
        if player_num not in [1, 2]:
            print("Invalid player number. Use 1 or 2.")
            return

        player_field = self.player1_field if player_num == 1 else self.player2_field
        player_graveyard = self.player1_graveyard if player_num == 1 else self.player2_graveyard

        dead_minions = [minion for minion in player_field if minion.health <= 0]

        for dead_minion in dead_minions:
            print(f"Player {player_num}'s {dead_minion.name} has died.")
            player_field.remove(dead_minion)
            player_graveyard.append(dead_minion)

    def __str__(self):
        board_str = f"Board State (Turn {self.game_turn}):\n"
        board_str += f"Player 1: {self.player1.health}/30 HP | {self.player1.mana_bar} Mana "
        board_str += " " * 60
        board_str += f"Player 2: {self.player2.health}/30 HP | {self.player2.mana_bar} Mana \n"
        board_str += f"Player 1 Deck: {len(self.player1.deck.cards)} cards\n"
        board_str += f"Player 2 Deck: {len(self.player2.deck.cards)} cards\n"
        board_str += f"Player 1 Hand: {len(self.player1_hand)} cards\n"
        board_str += f"Player 2 Hand: {len(self.player2_hand)} cards\n"
        board_str += f"Player 1 Field: {len(self.player1_field)} cards\n"
        board_str += f"Player 2 Field: {len(self.player2_field)} cards\n"
        board_str += f"Player 1 Graveyard: {len(self.player1_graveyard)} cards\n"
        board_str += f"Player 2 Graveyard: {len(self.player2_graveyard)} cards\n"
        return board_str


if __name__ == "__main__":
    player1_deck = get_test_deck("goblin")
    player2_deck = get_test_deck("gnome")

    player1 = Player(deck=player1_deck)
    player2 = Player(deck=player2_deck)

    # Create a board with the two decks
    board = Board(player1, player2)

    # Each player draws 7 cards
    for i in range(7):
        board.draw_card(1)
        board.draw_card(2)

    # Player 1 plays 3 cards
    board.play_card(1, 0)
    board.play_card(1, 0)
    board.play_card(1, 0)

    # Player 2 plays 3 cards
    board.play_card(2, 0)
    board.play_card(2, 0)
    board.play_card(2, 0)

    # print(board)

    board.attack_phase()

    print(board)
    print(board.player1.active_mana)

    board.attack_phase()

    print(board.player1.active_mana)

    print(board)

    print(board.player1.active_mana)
    print(board.player1.mana_bar)

    # Player 1 plays 3 cards
    board.play_card(1, 0)
    board.play_card(1, 0)
    board.play_card(1, 0)

    # Player 2 plays 3 cards
    board.play_card(2, 0)
    board.play_card(2, 0)
    board.play_card(2, 0)

    board.attack_phase()

    print(board)
