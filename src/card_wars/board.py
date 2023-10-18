from dataclasses import dataclass, field
from typing import List

from card_wars import logs
from card_wars.card import Card, Minion

log = logs.logger.info


# Overloaded list to update board state whenever list of minion on board changes
class FieldList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_board(self, board):
        print("update_board running!")
        if self is board.p1_field:
            board.check_board_buffs(self)
        elif self is board.p2_field:
            board.check_board_buffs(self)

    def append(self, item, board):
        if not isinstance(item, Minion):
            raise ValueError(f"Invalid type. Expected Minion, got {type(item).__name__}.")
        super().append(item)
        self.update_board(board)

    def extend(self, iterable, board):
        for item in iterable:
            if not isinstance(item, Minion):
                raise ValueError(f"Invalid type. Expected Minion, got {type(item).__name__}.")
        super().extend(iterable, board)
        self.update_board(board)

    def remove(self, item, board):
        print("debug Removing!!")
        super().remove(item)
        self.update_board(board)

    def pop(self, index, board):
        print("debug Popping!!")
        item = super().pop(index)
        self.update_board(board)
        return item

    def __delitem__(self, key, board):
        super().__delitem__(key)
        self.update_board(board)


@dataclass
class Board:
    """Holds minion field and graveyard for each player."""

    board_id: int = 0  # Used for GUI to select boards
    p1_field: FieldList = field(default_factory=FieldList)
    p2_field: FieldList = field(default_factory=FieldList)

    p1_board_buffs: List = field(default_factory=list)
    p2_board_buffs: List = field(default_factory=list)

    p1_grave: List[Card] = field(default_factory=list)
    p2_grave: List[Card] = field(default_factory=list)

    max_field_minion: int = 7

    # TODO entire check_board_buffs & apply_boar_buffs:
    # Make modular for all minion types, all buff types
    # For this to work we will have to refactor Minion(Card) class:
    # Load in default values for attack/health, pref as a tuple.
    # Then update current values in new attribute, similarly to how
    # health and max_health has its current relationship

    def check_board_buffs(self, player_field):
        """Called through update_board in FieldList"""
        print(f"Check board buffs running on {[m.name for m in player_field]}.")
        minions_on_field = [minion for minion in player_field if minion.health > 0]
        buff_list = self.p1_board_buffs if player_field == self.p1_field else self.p2_board_buffs

        # Clear buff list in Board class to avoid applying duplicate buffs when checking board
        buff_list = []

        for minion in minions_on_field:
            for ability in minion.ability:
                if isinstance(ability, str):
                    if ability == "divine_shield":
                        # No logic needed, handled in Minion take_damage only
                        print("Divine Shield found!")

                if isinstance(ability, str):
                    # Taunt not yet implemented # TODO
                    if ability == "taunt":
                        print("Taunt found!")

                elif isinstance(ability, dict):
                    #  Hard coded for testing purposes #TODO make modular for all board buffs
                    if (
                        ability.get("type") == "buff"
                        and ability.get("target") == "friendly"
                        and ability.get("target_race") == "Dragon"
                    ):
                        print("Dragon buff found!")

                        # Append any found buffs to Board class buff_list
                        buff_list.append(minion.ability)

        print(f"check_board_buffs finished:")
        print(buff_list)

        self.apply_board_buffs(player_field, buff_list)

    def apply_board_buffs(self, player_field, buff_list):
        print("Apply board buffs running.")
        minions_on_field = [minion for minion in player_field if minion.health > 0]
        print(f"{len(buff_list)} buffs found on board.")

        # Hard coded to health for testing purposes # TODO
        health_to_apply = 0
        for buffs in buff_list:
            health_to_apply += buffs[0].get("health", 0)

        for minion in minions_on_field:
            minion.health = minion.max_health + health_to_apply

            # TODO this does not take into account that the minion supplying
            # the buffs, also reveives the buffs itself. Must solve this some way.

    def add_to_field(self, minion: Minion, player_num):
        """
        Only for custom card interaction (summoning additional minions).
        For playing a card, instead call play_card in GameSession class.
        """
        if isinstance(minion, Minion):
            player_field = self.p1_field if player_num == 1 else self.p2_field
            if len(player_field) < self.max_field_minion:
                player_field.append(minion, self)
                log(f"{minion.name} summoned to P{player_num}'s field.")
                return
            else:
                log(f"Could not summon {minion.name}. Board is full!")
        else:
            raise ValueError("Invalid input. The input minion is not of type Minion.")

    def minions(self):
        for minion in self.p1_field + self.p2_field:
            yield minion

    def __len__(self):
        return sum(1 for _ in self.minions())

    def __str__(self):
        def format_minions(minions):
            return ", ".join([f"{m.name} [{m.attack}/{m.health}]" for m in minions])

        board_str = "Minions on board:\n"
        p1_field = format_minions(self.p1_field)
        p2_field = format_minions(self.p2_field)
        board_str += f"Player 1 Field: {p1_field}\n" if p1_field else "Player 1 Field is empty.\n"
        board_str += f"Player 2 Field: {p2_field}\n" if p2_field else "Player 2 Field is empty.\n"

        return board_str
