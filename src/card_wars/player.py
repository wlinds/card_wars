import random
from dataclasses import dataclass, field
from typing import List

from card_wars.card import Card
from card_wars.deck import Deck


@dataclass
class Player:
    name: str = f"P{random.randint(0,9)}"
    health: int = 30
    mana: int = 0
    deck: Deck = Deck()
    hand: List[Card] = field(
        default_factory=list
    )  # Maybe remove hand and hand size here and only use hand in Board class?
    max_hand_size: int = 10
    hero_power: str = None

    def __post_init__(self):
        # Format name
        self.name = self.name.strip()
        self.name = self.name.replace(".", "")
        self.name = self.name.replace(",", "")
        self.name = self.name.replace(" ", "_")


if __name__ == "__main__":
    test_player = Player(name="Mr. Test     ")
    print(test_player.name, "hello")
