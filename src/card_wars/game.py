import random
from dataclasses import dataclass, field
from typing import List

from card_wars import logs
from card_wars.board import Board
from card_wars.card import Card, Minion, Spell, Weapon, cast_spell
from card_wars.player import Player

log = logs.logger.info


@dataclass
class GameSession:
    player1: Player
    player2: Player
    board: Board
    player1_hand: List[Card] = field(default_factory=list)
    player2_hand: List[Card] = field(default_factory=list)
    player1_overdraw_dmg: int = 1
    player2_overdraw_dmg: int = 1

    game_turn: int = 0

    def end_turn(self):
        log(f"Turn {self.game_turn} ended.")

        self.game_turn += 1

        for p in [self.player1, self.player2]:
            if p.mana_bar < p.max_mana_bar:
                p.mana_bar += 1
            p.update_active_mana()

    def check_battlecry(self, card_to_play, player_num):
        player_field = self.board.p1_field if player_num == 1 else self.board.p2_field
        opponent_field = self.board.p2_field if player_num == 1 else self.board.p1_field

        for buff in card_to_play.buffs:
            # Check for AoE
            if isinstance(buff, dict) and buff.get("type") == "aoe":
                effect, value, target = buff.get("effect"), buff.get("value"), buff.get("target")
                # print(f"{target=}, {value=}, {effect=} n\ {card_to_play=}, {player_num=}")

                if effect == "damage":
                    if target == "all":
                        for minion in opponent_field + player_field:
                            minion.take_damage(value)
                    elif target == "friendly":
                        for minion in player_field:
                            minion.take_damage(value)
                    elif target == "enemy":
                        for minion in opponent_field:
                            minion.take_damage(value)
                elif effect == "healing":
                    pass
                    # TODO # Actually I wonder if we should do healing by just using negative values for damage methods(??)

            # Check for buff_friendly
            if isinstance(buff, dict) and buff.get("type") == "buff_friendly":
                attack, health, target = buff.get("attack"), buff.get("health"), buff.get("target")

                friendly_minions = [minion for minion in player_field if minion is not None]

                if friendly_minions and target == "random":
                    target_minion = random.choice(friendly_minions)
                    target_minion.health += health
                    target_minion.attack += attack
                    log(f"{player_field[0].name} received [+{attack}/+{health}]")

    def play_card(self, player_num, card_index):
        """
        Play a card from hand onto Board.
        player_num: 1 or 2 to indicate which player is playing.
        card_index: The index of the card in the player's hand to play.
        """

        player = self.player1 if player_num == 1 else self.player2
        player_hand = self.player1_hand if player_num == 1 else self.player2_hand
        player_field = self.board.p1_field if player_num == 1 else self.board.p2_field

        if not (0 <= card_index < len(player_hand)):
            print("Invalid card index.")
            return

        card_to_play = player_hand[card_index]

        if card_to_play:
            if player.active_mana >= card_to_play.mana_cost:
                if isinstance(card_to_play, Minion):
                    player_field.append(card_to_play)

                    log(
                        f"[+] Player {player_num} played: {card_to_play.name} "
                        f"[{card_to_play.attack}/{card_to_play.health}] Mana: {card_to_play.mana_cost} {card_to_play.card_text}"
                    )

                    # Check for aoe_battlecry #TODO Move and rename this method in separate script (?), have it check for all battlecries
                    self.check_battlecry(card_to_play, player_num)

                elif isinstance(card_to_play, Spell):
                    cast_spell(player, card_to_play.card_id)

                elif isinstance(card_to_play, Weapon):
                    player.equip_weapon(card_to_play)

                player.active_mana -= card_to_play.mana_cost
                del player_hand[card_index]

            else:
                print(f"Not enough mana to play {card_to_play.name}.")

        else:
            print("No card at selected index.")

    def draw_starting_cards(self, n=3):
        for player_num in [1, 2]:
            for _ in range(n):
                self.draw_card(player_num)

    def draw_card(self, player_num):
        """
        Draw a card from deck and add it to hand.
        player_num: 1 or 2 to indicate which player is drawing.
        """

        player = self.player1 if player_num == 1 else self.player2
        player_hand = self.player1_hand if player_num == 1 else self.player2_hand
        overdraw_damage = (
            self.player1_overdraw_dmg if player_num == 1 else self.player2_overdraw_dmg
        )

        if not player.deck.cards:
            log(
                f"Player {player_num} attempted do draw a card but has no cards left in their deck! Took {overdraw_damage} penalty damage!"
            )
            player.health -= overdraw_damage
            if player_num == 1:
                self.player1_overdraw_dmg += 1
            else:
                self.player2_overdraw_dmg += 1
            return

        drawn_card = player.deck.draw_card()
        player_hand.append(drawn_card)

        if isinstance(drawn_card, Minion):
            log(
                f"Player {player_num} drew: {drawn_card.name} [{drawn_card.attack}/{drawn_card.health}] Mana cost: {drawn_card.mana_cost}"
            )
        elif isinstance(drawn_card, Spell) or isinstance(drawn_card, Weapon):
            log(f"Player {player_num} drew: {drawn_card.name} Mana cost: {drawn_card.mana_cost}")

    def attack_phase(self):
        """
        Simulate the attack phase where minions on the field can attack each other and deal damage.
        Handle minion deaths and player health deduction.
        """

        self.attack_player_minions(player_num=1, target_player_num=2)
        self.attack_player_minions(player_num=2, target_player_num=1)

        player1_damage = sum(minion.attack for minion in self.board.p1_field)
        player2_damage = sum(minion.attack for minion in self.board.p2_field)

        if player1_damage != 0 or player2_damage != 0:
            self.player1.health -= player2_damage
            self.player2.health -= player1_damage

            if not self.board.p1_field:
                log("Player 1 has no minions left.")
                self.player2.health -= player1_damage
                log(f"Player 2 dealt {player2_damage} to enemy player.")

            if not self.board.p2_field:
                log("Player 2 has no minions left.")
                self.player1.health -= player2_damage
                log(f"Player 1 dealt {player1_damage} to enemy player.")

            log(f"{self.player1.health=}, {self.player2.health=}")

        self.end_turn()

    def attack_player_minions(self, player_num, target_player_num):
        """
        Simulate attacks from one player's minions to the other player's minions.
        """

        player_field = self.board.p1_field if player_num == 1 else self.board.p2_field
        target_player_field = self.board.p1_field if target_player_num == 1 else self.board.p2_field

        for attacking_minion in player_field:
            if target_player_field:
                target_minion = random.choice(target_player_field)
                attacking_minion.attack_target(target_minion)  # Use the attack_target method
                self.remove_dead_minions(player_num)
                self.remove_dead_minions(target_player_num)

    def remove_dead_minions(self, player_num):
        """
        Remove dead minions (health <= 0) from the player's field.
        """
        if player_num not in [1, 2]:
            print("Invalid player number. Use 1 or 2.")
            return

        player_field = self.board.p1_field if player_num == 1 else self.board.p2_field
        player_graveyard = self.board.p1_grave if player_num == 1 else self.board.p2_grave

        dead_minions = [minion for minion in player_field if minion.health <= 0]

        for dead_minion in dead_minions:
            log(f"Player {player_num}'s {dead_minion.name} has died.")
            player_field.remove(dead_minion)
            player_graveyard.append(dead_minion)

    def __str__(self):
        sep = " "
        width = 50
        game_str = f"\nGame State (Turn {self.game_turn}):\n \n"
        game_str += (
            self.player1.name
            + ((27 + width) - len(self.player1.name)) * sep
            + self.player2.name
            + "\n"
        )
        game_str += (
            f"{self.player1.health}/30 HP | {self.player1.active_mana}/{self.player1.mana_bar} Mana"
        )
        game_str += (
            (width + 8) * sep
            + f"{self.player2.health}/30 HP | {self.player2.active_mana}/{self.player2.mana_bar} Mana \n \n"
        )
        game_str += f"Player 1 Deck: {len(self.player1.deck.cards)} cards"
        game_str += (4 + width) * sep + f"Player 2 Deck: {len(self.player2.deck.cards)} cards\n"
        game_str += f"Player 1 Hand: {len(self.player1_hand)} cards"
        game_str += (5 + width) * sep + f"Player 2 Hand: {len(self.player2_hand)} cards\n"
        game_str += f"Player 1 Board: {len(self.board.p1_field)} minion(s)"
        game_str += (width) * sep + f"Player 2 Board: {len(self.board.p2_field)} minion(s)\n"
        # Yeah ik it's kinda cursed but

        return game_str
