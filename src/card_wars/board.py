from dataclasses import dataclass, field
from typing import List

from card_wars import logs
from card_wars.card import Card, Minion

log = logs.logger.info

# Class for Board. Only holds current Board (each player has one corresponding field).


@dataclass
class Board:
    board_id: int = 0  # Used for GUI to select boards
    p1_field: List[Card] = field(default_factory=list)
    p2_field: List[Card] = field(default_factory=list)
    p1_grave: List[Card] = field(default_factory=list)
    p2_grave: List[Card] = field(default_factory=list)

    max_field_minion: int = 7

    def add_to_field(self, minion: Minion, player_num):
        """
        Only for custom card interaction (summoning additional minions).
        For playing a card, instead call play_card in GameSession class.
        """
        if isinstance(minion, Minion):
            player_field = self.p1_field if player_num == 1 else self.p2_field
            player_field.append(minion)
            log(f"{minion.name} summoned to P{player_num}'s field.")
            return
        else:
            raise ValueError("Invalid input. The input minion is not of type Minion.")

    def __str__(self):
        def format_minions(minions):
            return ", ".join(
                [f"{minion.name} [{minion.attack}/{minion.health}]" for minion in minions]
            )

        board_str = "Minions on board:\n"

        p1_field = format_minions(self.p1_field)
        p2_field = format_minions(self.p2_field)

        board_str += f"Player 1 Field: {p1_field}\n" if p1_field else "Player 1 Field is empty.\n"
        board_str += f"Player 2 Field: {p2_field}\n" if p2_field else "Player 2 Field is empty.\n"

        return board_str

    def __len__(self):
        return sum(1 for _ in self.minions())

    def minions(self):
        for minion in self.p1_field + self.p2_field:
            yield minion
