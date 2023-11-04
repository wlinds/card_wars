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
    game_turn: int = 0

    # player1_hand: List[Card] = field(default_factory=list) # Now in Player class
    # player2_hand: List[Card] = field(default_factory=list)
    # player1_overdraw_dmg: int = 1 # Now in Player class
    # player2_overdraw_dmg: int = 1

    def add_to_hand(self, player_num, card):  # Has been migrated to Player class
        """Add a copy of any card to player hand."""
        player, player_hand, _, _, _ = self.get_player(player_num)

        if card is not None:
            if len(player_hand) < player.max_hand_size:
                player_hand.append(card)
            else:
                log(f"Hand full! {card.name} was discarded.")

    def get_all_targets(self, player_num=None) -> list:
        """
        Returns all targets if player_num = None,
        else returns opponent player field minion(s) and opponent player as target.
        """
        targets = []
        targets.extend(self.board.p2_field if player_num == 1 or player_num is None else [])
        targets.append(self.player2 if player_num == 1 or player_num is None else None)
        targets.extend(self.board.p1_field if player_num == 2 or player_num is None else [])
        targets.append(self.player1 if player_num == 2 or player_num is None else None)

        return targets

    def target_assist(self, player_num, all_random=True, all_enemy=False, all_friendly=False):
        """
        Call when an action requires a target but no target is provided.
        """
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

        if isinstance(selected_target, Player):
            log(f"[Target Assist running] Selected target: {selected_target.name}.")

        return selected_target

    def end_turn(self):
        self.game_turn += 1
        for p in [self.player1, self.player2]:
            if p.mana_bar < p.max_mana_bar:
                p.mana_bar += 1
            p.update_active_mana()
        log(f"Turn {self.game_turn} ended.")

    # TODO simplify this (move to new script)
    def get_player(self, player_num):
        """Returns player, player_hand, player_field, opponent_field, player_graveyard"""
        p = self.player1 if player_num == 1 else self.player2
        ph = p.hand
        pf = self.board.p1_field if player_num == 1 else self.board.p2_field
        of = self.board.p2_field if player_num == 1 else self.board.p1_field
        pg = self.board.p1_grave if player_num == 1 else self.board.p2_grave
        return p, ph, pf, of, pg

    # TODO simplify this, refactor, better var names (move to new script)
    def check_battlecry(self, card_to_play, player_num, select_target=None):
        player, player_hand, player_field, opponent_field, _ = self.get_player(player_num)

        for buff in card_to_play.battlecry:
            # Check for merge
            if isinstance(buff, dict) and buff.get("type") == "merge":
                target = buff.get("target")
                if target == "friendly":
                    print("merging")
                    print(card_to_play, select_target)
                    card_to_play += select_target
                    player_field.remove(select_target, self.board)
                    return card_to_play

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
                        characters_to_heal = self.target_assist(
                            player_num, all_random=False, all_enemy=False, all_friendly=True
                        )

                        for character in characters_to_heal:
                            character.heal(value=value)
                            log(f"{character.name} was healed for {value}")

                # Check fo AoE buff
                elif effect == "buff" and target != "any":
                    for minion in player_field:
                        if minion.race == target:
                            minion.health[0] += value[1]
                            minion.health[1] += value[1]  # TODO
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
                    target_minion.health[0] += health
                    target_minion.health[1] += health
                    target_minion.attack += attack
                    log(f"{target_minion.name} received [+{attack}/+{health}]")

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

                self.add_to_hand(player_num, find_card(target))
                log(f"{find_card(target).name} added to P{player_num}'s hand")

            # Check for buff_summon
            if isinstance(buff, dict) and buff.get("type") == "summon":
                self.board.add_to_field(find_card(buff.get("card_id")), player_num)

            # Check for mana_burn
            if isinstance(buff, dict) and buff.get("type") == "mana_burn":
                if buff.get("target") == "self" and buff.get("effect") == "buff":
                    card_to_play.attack += buff.get("attack") * player.mana_bar

                    # Updating health twice like this is tedious, should fix TODO
                    card_to_play.health[0] += player.mana_bar * buff.get("health")
                    card_to_play.health[1] += player.mana_bar * buff.get("health")

                else:
                    # TODO Cards that target enemies here
                    pass

                # Reset mana bar
                player.mana_bar = 0
                # Account for cost of playing card
                player.active_mana = card_to_play.get_mana()

        #         {
        #   "type": "burn_mana",
        #   "effect": "buff",
        #   "attack": 1,
        #   "health": 1,
        #   "repeat": "mana_bar",
        #   "target": "self"
        # }

        self.remove_dead_minions(1)
        self.remove_dead_minions(2)

        return card_to_play

        return card_to_play

    def play_card(self, player_num, card_index, select_target=None):  # Select target TODO
        """
        Play a card from hand onto Board.
        player_num: 1 or 2 to indicate which player is playing.
        card_index: The index of the card in the player's hand to play.
        """

        player, player_hand, player_field, opponent_field, _ = self.get_player(player_num)

        # Case when method receives negative index values (for playing last drawn card etc.)
        if card_index < 0:
            card_index += len(player_hand)

        if not (0 <= card_index < len(player_hand)):
            print("Invalid card index.")
            return

        card_to_play = player_hand[card_index]
        print(card_to_play)

        if isinstance(card_to_play, Minion) and len(player_field) >= self.board.max_field_minion:
            print(f"Cannot play {card_to_play.name}. Board is full!")
            return

        if card_to_play:
            if player.active_mana >= card_to_play.mana_cost:
                if isinstance(card_to_play, Minion):
                    for buff in card_to_play.battlecry:
                        if isinstance(buff, dict) and buff.get("target") == "any":
                            if select_target == None:
                                print("Must select a target!")
                                select_target = self.target_assist(player_num, all_random=True)
                            break
                    log(
                        f"[+] Player {player_num} played: {card_to_play.name} "
                        f"[{card_to_play.attack}/{card_to_play.health[0]}] Mana: {card_to_play.mana_cost} {card_to_play.card_text}"
                    )

                    card_to_play = self.check_battlecry(card_to_play, player_num, select_target)

                    player_field.append(card_to_play, self.board)

                elif isinstance(card_to_play, Spell):
                    self.cast_spell(player_num, card_to_play)
                    # TODO add to graveyard

                elif isinstance(card_to_play, Weapon):
                    player.equip_weapon(card_to_play)
                    # TODO add to graveyard

                player.active_mana -= card_to_play.mana_cost
                del player_hand[card_index]

            else:
                print(f"Not enough mana to play {card_to_play.name}.")

        else:
            print("No card at selected index.")

    def cast_spell(self, player_num, card, target=None):
        log(f"Player {player_num} cast {card.name}")

        if card.card_id == "sfro000":
            target = self.target_assist(player_num=player_num, all_random=False, all_enemy=True)
            for entity in target:
                entity.take_damage(card.damage)

            self.remove_dead_minions(1)
            self.remove_dead_minions(2)

    def draw_starting_cards(self, n=3):
        for player_num in [1, 2]:
            for _ in range(n):
                self.draw_card(player_num)

    def draw_card(self, player_num):  # Has been migrated to Player class
        """
        Draw a card from deck and add it to hand.
        player_num: 1 or 2 to indicate which player is drawing.
        """

        player, _, _, _, _ = self.get_player(player_num)

        if not player.deck.cards:
            log(
                f"Player {player_num} attempted do draw a card but has no cards left in their deck!"
            )
            player.take_damage(player.overdraw_damage)
            if player_num == 1:
                player.overdraw_damage += 1
            else:
                player.overdraw_damage += 1
            return

        drawn_card = player.deck.draw_card()

        if isinstance(drawn_card, Minion):
            log(
                f"Player {player_num} drew: {drawn_card.name} [{drawn_card.attack}/{drawn_card.health[0]}] Mana cost: {drawn_card.mana_cost}"
            )
        elif isinstance(drawn_card, Spell) or isinstance(drawn_card, Weapon):
            log(f"Player {player_num} drew: {drawn_card.name} Mana cost: {drawn_card.mana_cost}")

        self.add_to_hand(player_num, drawn_card)

    def attack_phase(self):
        """
        Simulate the attack phase where minions on the field can attack each other and deal damage.
        Handle minion deaths and player health deduction.
        """

        # TODO have each player's minion take turn attacking instead
        self.attack_player_minions(player_num=1, target_player_num=2)
        self.attack_player_minions(player_num=2, target_player_num=1)

        player1_damage = sum(minion.attack for minion in self.board.p1_field)
        player2_damage = sum(minion.attack for minion in self.board.p2_field)

        if player1_damage != 0 or player2_damage != 0:
            self.player1.health[0] -= player2_damage
            self.player2.health[0] -= player1_damage

            if not self.board.p1_field:
                log("Player 1 has no minions left.")
                self.player2.health[0] -= player1_damage
                log(f"Player 2 dealt {player2_damage} to enemy player.")

            if not self.board.p2_field:
                log("Player 2 has no minions left.")
                self.player1.health[0] -= player2_damage
                log(f"Player 1 dealt {player1_damage} to enemy player.")

            log(f"{self.player1.health[0]=}, {self.player2.health[0]=}")

        self.end_turn()

    def attack_player_minions(self, player_num, target_player_num):
        """
        Simulate attacks from one player's minions to the other player's minions.
        """

        # TODO bug where not all minions always attacks (??)
        # This should be refactored anyway (indcluding attack_phase)

        _, _, player_field, opponent_field, _ = self.get_player(player_num)

        # This line below is caused because irregularity in ability value (sometimes dictionary, sometimes string)
        taunt_minions = [
            minion
            for minion in opponent_field
            if not any(isinstance(ability, dict) for ability in minion.ability)
            and any("taunt" in str(ability).lower() for ability in minion.ability)
        ]

        if taunt_minions:
            for attacking_minion in player_field:
                for target_minion in taunt_minions:
                    attacking_minion.attack_target(target_minion)
                    self.remove_dead_minions(player_num)
                    self.remove_dead_minions(target_player_num)

                    # Same thing here ugh
                    if not any(
                        "taunt" in ability.lower() if isinstance(ability, str) else False
                        for minion in opponent_field
                        for ability in minion.ability
                    ):
                        break
        else:
            for attacking_minion in player_field:
                if opponent_field:
                    target_minion = random.choice(opponent_field)
                    attacking_minion.attack_target(target_minion)
                    self.remove_dead_minions(player_num)
                    self.remove_dead_minions(target_player_num)

    def remove_dead_minions(self, player_num):
        """
        Remove dead minions (health <= 0) from the player's field.
        """
        (
            _,
            _,
            player_field,
            _,
            player_graveyard,
        ) = self.get_player(player_num)
        dead_minions = [minion for minion in player_field if minion.health[0] <= 0]

        if dead_minions == None:
            return

        # First remove all minions with hp <= 0
        for m in dead_minions:
            log(f"Player {player_num}'s {m.name} has died.")

            # This should probably be a method instead
            player_field.remove(m, self.board)
            player_graveyard.append(m)

        # Then check for deathrattles
        for dead_minion in dead_minions:
            for buff in dead_minion.deathrattle:
                # Summoning deathrattles
                if isinstance(buff, dict) and buff.get("type") == "summon":
                    log(f"{dead_minion.name} triggered its deathrattle:")
                    self.board.add_to_field(find_card(buff.get("card_id")), player_num)

                # Deal damage deathrattle
                if isinstance(buff, dict) and buff.get("type") == "deathrattle_damage":
                    # Minion specific log text. This really should be in another script..
                    if dead_minion.card_id == "mgob002":
                        log(
                            f"{dead_minion.name} triggered its deathrattle. Here comes {buff.get('repeat', 1)} knifes!:"
                        )
                    else:
                        log(f"{dead_minion.name} triggered its deathrattle!")
                    value, repeat = buff.get("value"), buff.get("repeat", 1)
                    for i in range(repeat):
                        all_possible_targets = self.get_all_targets()
                        target = random.choice(all_possible_targets)
                        target.take_damage(value)

                        self.remove_dead_minions(1)
                        self.remove_dead_minions(2)

                if isinstance(buff, dict) and buff.get("type") == "share_stat":
                    stat, target = buff.get("stat"), buff.get("target")
                    share_stat = getattr(dead_minion, stat)
                    if share_stat == dead_minion.health and target == "friendly_minion":
                        if len(player_field) > 0:
                            m = random.choice(player_field)

                            # TODO - not update stats like this..
                            m.health[0] += share_stat[1]
                            m.health[1] += share_stat[1]

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
        game_str += f"{self.player1.health[0]}/{self.player1.max_health} HP | {self.player1.active_mana}/{self.player1.mana_bar} Mana"
        game_str += (
            (width + 8) * sep
            + f"{self.player2.health[0]}/{self.player2.max_health} HP | {self.player2.active_mana}/{self.player2.mana_bar} Mana \n \n"
        )
        add_space = 1 if len(self.player1.deck.cards) < 10 else 0
        game_str += f"Player 1 Deck: {len(self.player1.deck.cards)} cards"
        game_str += (
            (4 + width) * sep
            + (" " * add_space)
            + f"Player 2 Deck: {len(self.player2.deck.cards)} cards\n"
        )
        game_str += f"Player 1 Hand: {len(self.player1.hand)} cards"
        game_str += (5 + width) * sep + f"Player 2 Hand: {len(self.player2.hand)} cards\n"
        game_str += f"Player 1 Board: {len(self.board.p1_field)} minion(s)"
        game_str += (width) * sep + f"Player 2 Board: {len(self.board.p2_field)} minion(s)\n"

        # Yeah ik it's kinda cursed but

        return game_str
