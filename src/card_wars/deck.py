import json
import random
from dataclasses import dataclass, field
from typing import List

from card_wars.card import *
from card_wars.import_cards import find_card, get_all_cards, read_cards_from


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


def get_test_deck(deck_type: str = "goblin") -> Deck:
    test_deck = Deck()
    if deck_type == "goblin":
        test_deck.fill_with_card(find_card("m00"))

    elif deck_type == "gnome":
        test_deck.fill_with_card(find_card("m02"))

    elif deck_type == "random":
        all_cards_list = get_all_cards()
        for i in range(test_deck.card_limit):
            test_deck.add_card(all_cards_list[random.randint(0, len(all_cards_list) - 1)])

    else:
        print('Invalid parameter. Try "goblin" or "gnome".')
        return

    return test_deck


if __name__ == "__main__":
    goblin_deck = get_test_deck("goblin")
    gnome_deck = get_test_deck("goblin")
    random_deck = get_test_deck("random")
    print(random_deck)
