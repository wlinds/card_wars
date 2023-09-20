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
    hand: List[Card] = field(default_factory=list)
    max_hand_size: int = 10
    hero_power: str = None

    def draw_card(self):
        if len(self.hand) < self.max_hand_size:
            card = self.deck.draw_card()
            if card:
                self.hand.append(card)
        else:
            print("Hand is full. Cannot draw more cards.")


if __name__ == "__main__":
    player_test = Player()
    print(player_test.name)
    player_test.draw_card()
