import json
import random
from dataclasses import dataclass, field
from typing import List

from src.card_wars.card import *
from src.card_wars.import_cards import read_cards_from


@dataclass
class Deck:
    name: str = "Default Deck"
    card_limit: int = 30
    cards: List[Card] = field(default_factory=list)

    def add_card(self, card: Card):
        if len(self.cards) < self.card_limit:
            self.cards.append(card)
        else:
            print("Deck is full. Cannot add more cards.")

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if self.cards:
            return self.cards.pop(0)  # Remove and return the top card from the deck
        else:
            print("Deck is empty. Cannot draw a card.")

    def fill_with_card(self, card: Card):
        """
        Fill the deck with a specific card until the deck limit is reached.
        """
        while len(self.cards) < self.card_limit:
            self.cards.append(card)

    def __str__(self):
        deck_str = f"{self.name} - {len(self.cards)} cards:\n"
        for card in self.cards:
            deck_str += f"  {card}\n"
        return deck_str


if __name__ == "__main__":
    pass