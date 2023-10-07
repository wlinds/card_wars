import copy
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
        assert isinstance(
            card, Card
        ), "'card' argument must be an instance of the 'Card' class. Did you enter a string?"

        if len(self.cards) < self.card_limit:
            # Create a new instance of the card and add it to the deck
            new_card = copy.deepcopy(card)
            self.cards.append(new_card)
        else:
            print(f"Deck is full ({self.card_limit} cards). Cannot add more cards.")

    def shuffle(self):
        if self.cards == []:
            print("Cannot shuffle empty deck.")
        else:
            random.shuffle(self.cards)

    def draw_card(self):
        """
        Regular draw method. This removes the card from the deck.
        """
        if self.cards:
            return self.cards.pop(0)  # Remove and return the top card from the deck
        else:
            print("Deck is empty. Cannot draw a card.")

    def fill_with_card(self, card: Card):
        """
        Fill the deck with a specific card until the deck limit is reached.
        """

        while len(self.cards) < self.card_limit:
            # Create a new instance of the card and add it to the deck
            new_card = copy.deepcopy(card)
            self.cards.append(new_card)

    def get_card(self, index: int) -> Card:
        """
        Get the card at a specific index in the deck.
        This does not remove the card from the deck.
        """
        if 0 <= index < len(self.cards):
            return self.cards[index]
        else:
            print(f"Invalid index {index}. Must be in range [0, {len(self.cards) - 1}]")

    def burn_deck(self):
        """
        Remove all cards in deck.
        """
        self.cards = []

    def __str__(self):
        deck_str = f"{self.name} - {len(self.cards)} cards:\n"
        for card in self.cards:
            deck_str += f"  {card.card_id, card.name}\n"
        return deck_str


def get_test_deck(deck_type: str = "goblin") -> Deck:
    test_deck = Deck()
    if deck_type == "goblin":
        test_deck.fill_with_card(find_card("mgob000"))

    elif deck_type == "gnome":
        test_deck.fill_with_card(find_card("mgno000"))

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
    goblin_deck.burn_deck()
    goblin_deck.add_card("asdf")
