import random
from dataclasses import dataclass, field
from typing import List

from card_wars import logs
from card_wars.board import Board
from card_wars.card import Card, Minion, Spell, Weapon
from card_wars.import_cards import find_card
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

    def get_target(self, player_num, all_random=True, all_enemy=False, all_friendly=False):
        selected_target = []

        if all_random:
            targets = [self.player1, self.player2]
            all_minions = self.board.p1_field + self.board.p2_field

            if all_minions:
                selected_target = random.choice(all_minions)
            else:
                selected_target = random.choice(targets)

        if all_enemy:
            if player_num == 1:
                enemy_minions = self.board.p2_field
                selected_target.append(self.player2)
                selected_target.extend(enemy_minions)
            else:
                enemy_minions = self.board.p1_field
                selected_target.append(self.player1)
                selected_target.extend(enemy_minions)

        if all_friendly:
            if player_num == 1:
                friendly_minions = self.board.p1_field
                selected_target.append(self.player1)
                selected_target.extend(friendly_minions)

        log(f"[Target Assist running] Selected target: {selected_target}.")

        return selected_target

    def end_turn(self):
        log(f"Turn {self.game_turn} ended.")

        self.game_turn += 1

        for p in [self.player1, self.player2]:
            if p.mana_bar < p.max_mana_bar:
                p.mana_bar += 1
            p.update_active_mana()

    def check_battlecry(self, card_to_play, player_num, select_target=None):
        player = self.player1 if player_num == 1 else self.player2
        player_hand = self.player1_hand if player_num == 1 else self.player2_hand
        player_field = self.board.p1_field if player_num == 1 else self.board.p2_field
        opponent_field = self.board.p2_field if player_num == 1 else self.board.p1_field

        for buff in card_to_play.buffs:
            # Check for deal_damage battlecry
            if isinstance(buff, dict) and buff.get("type") == "deal_damage":
                value, target = buff.get("value"), buff.get("target")
                if target == "any":
                    assert select_target != None
                    select_target.take_damage(value)

            # Check for AoE damage
            if isinstance(buff, dict) and buff.get("type") == "aoe":
                effect, value, target = buff.get("effect"), buff.get("value"), buff.get("target")

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

                # Check for AoE healing
                elif effect == "healing":
                    if target == "friendly":
                        characters_to_heal = self.get_target(
                            player_num, all_random=False, all_enemy=False, all_friendly=True
                        )

                        for character in characters_to_heal:
                            character.heal(value=value)
                            log(f"{character.name} was healed for {value}")

                # Check fo AoE buff
                elif effect == "buff" and target != "any":
                    for minion in player_field:
                        if minion.race == target:
                            minion.max_health += value[1]  # TODO
                            minion.health += value[1]
                            minion.attack += value[0]
                            log(
                                f"{minion.name} received [+{value[0]}/+{value[1]}] from {card_to_play.name}."
                            )

            # Check for buff_friendly
            if isinstance(buff, dict) and buff.get("type") == "buff_friendly":
                attack, health, target = buff.get("attack"), buff.get("health"), buff.get("target")

                friendly_minions = [minion for minion in player_field if minion is not None]

                if friendly_minions and target == "random":
                    target_minion = random.choice(friendly_minions)
                    target_minion.health += health
                    target_minion.attack += attack
                    log(f"{player_field[0].name} received [+{attack}/+{health}]")

            # Check for draw
            if isinstance(buff, dict) and buff.get("type") == "draw":
                self.draw_card(player_num)

            # Check for card_generation
            if isinstance(buff, dict) and buff.get("type") == "generate_card":
                target = buff.get("target")
                if target == "random_same_race":
                    minion_pool = find_card(minion_race=(card_to_play.race))
                    target = random.choice(minion_pool)
                    target = target.card_id

                if len(player_hand) < player.max_hand_size:
                    print(f"{target} added to {player.name} hand.")
                    player_hand.append(find_card(buff.get(target)))

            # Check for buff_summon
            if isinstance(buff, dict) and buff.get("type") == "buff_summon":
                self.board.add_to_field(find_card(buff.get("card_id")), player_num)

        self.remove_dead_minions(1)
        self.remove_dead_minions(2)

    def play_card(self, player_num, card_index, select_target=None):  # Select target TODO
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

        if isinstance(card_to_play, Minion) and len(player_field) >= self.board.max_field_minion:
            print(f"Cannot play {card_to_play.name}. Board is full!")
            return

        if card_to_play:
            if player.active_mana >= card_to_play.mana_cost:
                if isinstance(card_to_play, Minion):
                    for buff in card_to_play.buffs:
                        if isinstance(buff, dict) and buff.get("target") == "any":
                            print("Must select a target!")
                            select_target = self.get_target(player_num, all_random=True)
                            break
                    log(
                        f"[+] Player {player_num} played: {card_to_play.name} "
                        f"[{card_to_play.attack}/{card_to_play.health}] Mana: {card_to_play.mana_cost} {card_to_play.card_text}"
                    )

                    self.check_battlecry(card_to_play, player_num, select_target)

                    player_field.append(card_to_play)

                elif isinstance(card_to_play, Spell):
                    self.cast_spell(player_num, card_to_play)

                elif isinstance(card_to_play, Weapon):
                    player.equip_weapon(card_to_play)

                player.active_mana -= card_to_play.mana_cost
                del player_hand[card_index]

            else:
                print(f"Not enough mana to play {card_to_play.name}.")

        else:
            print("No card at selected index.")

    def cast_spell(self, player_num, card, target=None):
        log(f"Player {player_num} cast {card.name}")

        if card.card_id == "sfro000":
            target = self.get_target(player_num=player_num, all_random=False, all_enemy=True)
            for entity in target:
                entity.take_damage(card.damage)

            self.remove_dead_minions(1)
            self.remove_dead_minions(2)

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
                f"Player {player_num} attempted do draw a card but has no cards left in their deck!"
            )
            player.take_damage(overdraw_damage)
            if player_num == 1:
                self.player1_overdraw_dmg += 1
            else:
                self.player2_overdraw_dmg += 1
            return

        drawn_card = player.deck.draw_card()

        if isinstance(drawn_card, Minion):
            log(
                f"Player {player_num} drew: {drawn_card.name} [{drawn_card.attack}/{drawn_card.health}] Mana cost: {drawn_card.mana_cost}"
            )
        elif isinstance(drawn_card, Spell) or isinstance(drawn_card, Weapon):
            log(f"Player {player_num} drew: {drawn_card.name} Mana cost: {drawn_card.mana_cost}")

        if len(player_hand) < player.max_hand_size:
            player_hand.append(drawn_card)

        else:
            log(f"Player hand is full! {drawn_card.name} was discarded.")

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

        if dead_minions == None:
            return

        for dead_minion in dead_minions:
            log(f"Player {player_num}'s {dead_minion.name} has died.")
            player_field.remove(dead_minion)
            player_graveyard.append(dead_minion)

            # Check deathrattles
            for buff in dead_minion.buffs:
                if isinstance(buff, dict) and buff.get("type") == "deathrattle_summon":
                    log(f"{dead_minion.name} triggerd deathrattle:")
                    self.board.add_to_field(find_card(buff.get("card_id")), player_num)

                if isinstance(buff, dict) and buff.get("type") == "deathrattle_damage":
                    log(f"{dead_minion.name} triggerd deathrattle. Here comes knifes!:")
                    value, repeat = buff.get("value"), buff.get("repeat", 1)
                    for i in range(repeat):
                        target = self.get_target(player_num)
                        target.take_damage(value)

        if dead_minions:
            self.remove_dead_minions(player_num)

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
