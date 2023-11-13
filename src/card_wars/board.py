from dataclasses import dataclass, field
from typing import List

from card_wars import logs
from card_wars.card import Card, Minion
from card_wars.deck import get_test_deck
from card_wars.import_cards import find_card
from card_wars.player import Player

log = logs.logger.info


# Overloaded list to update board state whenever list of minion on board changes
# Each player has their own FieldList. This is the home of their minions on board.


class FieldList(list):
    def __init__(self, *args, field_name="Default Player Field", **kwargs):
        self.field_name = field_name
        super().__init__(*args, **kwargs)

    # Not sure if we need to do this, instead we check all minion on both
    def update_board(self, board):
        if self is board.p1_field:
            print("debug - calling check_board_buffs on p1_field")
        elif self is board.p2_field:
            print("debug - calling check_board_buffs on p2_field")
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
        super().remove(item)
        self.update_board(board)

    def pop(self, index, board):
        item = super().pop(index)
        self.update_board(board)
        return item

    def __delitem__(self, key, board):
        super().__delitem__(key)
        self.update_board(board)

    def __str__(self):
        return f"Field - {self.field_name}:\n" + "\n".join(m.name for m in self)

    def __getitem__(self, index):
        return super().__getitem__(index)


@dataclass
class Board:
    """Holds minion field and graveyard for each player."""

    board_id: int = 0  # Used for GUI to select boards
    p1_field: FieldList = field(default_factory=lambda: FieldList(field_name="P1"))
    p2_field: FieldList = field(default_factory=lambda: FieldList(field_name="P2"))

    p1_grave: List[Card] = field(default_factory=list)
    p2_grave: List[Card] = field(default_factory=list)

    max_field_minion: int = 7

    # Both check_board_buffs and apply_board_buffs are still kinda clunky.
    # They work, but yeah, but should try to refactor + also need to impl new buffs

    def check_board_buffs(self, player_field):
        """Called through update_board in FieldList"""
        minions_on_field = [minion for minion in player_field]

        for minion in minions_on_field:
            if minion.ability == [] or minion.ability == "":
                print(f"Debug: No abilities on {player_field.field_name} board")
                return

        board_buff_list = []

        for minion in minions_on_field:
            board_buff_list += [
                ability
                for ability in minion.ability
                if isinstance(ability, dict) and ability.get("type") == "board_buff"
            ]

        self.apply_board_buffs(player_field, board_buff_list)

    def apply_board_buffs(self, player_field, board_buff_list):
        # Reset buff stats for all minion to avoid duplicate buffs
        for minion in player_field:
            minion.mod_stats = [0, 0, 0]

        target_field = self.p1_field if player_field == self.p2_field else self.p2_field
        minions_on_field = [minion for minion in player_field]

        def update_mod_stats(minion, buffs):
            minion.mod_stats[0] += buffs.get("attack", 0)
            minion.mod_stats[1] += buffs.get("health", 0)
            minion.mod_stats[2] += buffs.get("mana", 0)

        for minion in minions_on_field:
            for buffs in board_buff_list:
                print(buffs)
                if buffs.get("target") == "friendly":
                    if minion.race == buffs.get("target_race"):
                        print(f"Updating buffs on {buffs.get('target_race')}")
                        update_mod_stats(minion, buffs)

                    elif buffs.get("target_race") == "all":
                        print(f"Updating buffs on {minion}")
                        update_mod_stats(minion, buffs)

                elif buffs.get("target") == "enemy":
                    for minion in target_field:
                        if minion.race == buffs.get("target_race"):
                            print(f"Updating buffs on {buffs.get('target_race')}")
                            update_mod_stats(minion, buffs)

                        elif buffs.get("target_race") == "all":
                            print(f"Updating buffs on {minion.name}")
                            update_mod_stats(minion, buffs)

        # TODO this does not take into account that the minion supplying
        # the buffs also receives the buffs itself. Might wanna solve this some way.

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
            raise ValueError("Invalid argument. The input minion is not of type Minion.")

    def remove(self, player_field, idx):
        """
        Only for custom card interaction.
        For removing dead minions, instead call remove_deaa_minnions in GameSession.
        """
        field = self.p1_field if player_field == 1 else self.p2_field
        print(f"{field[idx].name} was removed.")
        field.__delitem__(idx, self)

    def minions(self):
        for minion in self.p1_field + self.p2_field:
            yield minion

    def __len__(self):
        return sum(1 for _ in self.minions())

    def __str__(self):
        if self.p1_field == [] and self.p2_field == []:
            return "Board is empty."

        def format_minions(minions):
            return ", ".join([f"{m.name} [{m.get_attack()}/{m.get_health()[0]}]" for m in minions])

        board_str = "Minions on board:\n"
        p1_field = format_minions(self.p1_field)
        p2_field = format_minions(self.p2_field)
        board_str += f"Player 1 Field: {p1_field}\n" if p1_field else "Player 1 Field is empty.\n"
        board_str += f"Player 2 Field: {p2_field}\n" if p2_field else "Player 2 Field is empty.\n"

        return board_str


if __name__ == "__main__":
    board = Board()
    buff_dragon = find_card("mdra001")
    for _ in range(3):
        board.add_to_field(buff_dragon, 2)

    print(board)

    for _ in range(3):
        print(board.p2_field[_].mod_stats)

    board.remove(2, 0)
    print(board.p2_field[0].mod_stats)

    board.add_to_field(find_card("mgob000"), 2)
    board.add_to_field(find_card("mdem000"), 1)

    print(board)

    print(board.p2_field[2].mod_stats)

    board.add_to_field(find_card("mdem000"), 1)

    print(board.p2_field[2].mod_stats)

    deck = get_test_deck()
    board.add_to_field(deck[0], 1)
    board.add_to_field(deck[-1], 1)
    board.add_to_field(deck[-2], 1)
    board.add_to_field(deck[1], 2)

    print(board)

    board.p1_field.field_name = "just a field name"
    # print(board.p1_field)

    minion1 = board.p1_field[0]
    minion2 = board.p2_field[0]

    minion1.attack_target(minion2, attack_mod=999)

    print(board)

    # # Actually this is probably a way better method than remove_dead_minion in game class...
    # for player_field, field, player_grave in [(1, board.p1_field, board.p1_grave), (2, board.p2_field, board.p2_grave)]:
    #     for idx, minion in enumerate(field):
    #         if minion.health[0] <= 0:
    #             player_grave.append(minion)
    #             board.remove(player_field, idx)

    field = list(board.p2_field)
    for minion in field:
        if minion.health[0] <= 0:
            board.p2_grave.append(minion)
            idx = board.p2_field.index(minion)
            board.remove(2, idx)

    field = list(board.p1_field)
    for minion in field:
        if minion.health[0] <= 0:
            board.p1_grave.append(minion)
            idx = board.p1_field.index(minion)
            board.remove(1, idx)

    print(len(board))
    print(board)

    board.remove(board.p2_field, 0)

    print(board)

    print(len(board.p1_grave), len(board.p2_grave))
    merged_minion = board.p1_field[2] + board.p1_field[0]

    print(repr(merged_minion))
    print(merged_minion.card_text)

    board.remove(1, 0)
    board.remove(1, 0)

    board.add_to_field(merged_minion, 1)

    print(board)
