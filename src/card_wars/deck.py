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
        """
        Add a copy of any card to deck card list.
        """
        if isinstance(card, str):
            card = find_card(card)

        if card is not None:
            if len(self.cards) < self.card_limit:
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

    def fill_with_card(self, card: Card, fill: float = 1.0):
        """
        Fill the deck with a specific card until the deck limit is reached.
        """
        if fill <= 0.0:
            return

        max_deck = int(self.card_limit * fill)

        if max_deck > self.card_limit:
            max_deck = self.card_limit

        cards_to_add = max_deck - len(self.cards)

        for _ in range(cards_to_add):
            new_card = copy.deepcopy(card)
            self.add_card(new_card)

        print(f"Added {cards_to_add} copies of {card}")

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

    def remove_card(self, card_input):
        """
        Remove all copies of a specified card from the card list based on user input.
        """
        if isinstance(card_input, int):  # Check if the input is an integer (card index)
            if 0 <= card_input < len(self.cards):
                removed_card = self.cards.pop(card_input)
                print(f"Removed card at index {card_input}: '{removed_card}'")
            else:
                print("Invalid card index. Please enter a valid index.")
        elif isinstance(card_input, str):  # Check if the input is a string (card name)
            card = find_card(card_input)
            if card is not None:
                self.cards = [c for c in self.cards if c.card_id != card.card_id]
                print(f"Removed all copies of '{card}' from the deck.")
            else:
                print(f"Card '{card_input}' not found.")
        elif isinstance(card_input, Card):  # Check if the input is a Card object
            card_id = card_input.card_id
            self.cards = [c for c in self.cards if c.card_id != card_id]
            print(f"Removed all copies of '{card_input}' from the deck.")
        else:
            print("Invalid input. Please enter a card name, card index, or provide a Card object.")

    def __str__(self):
        deck_str = f"{self.name} - [{len(self.cards)}/{self.card_limit}] cards:\n"

        for card in self.cards:
            if card is not None:
                deck_str += f"  {card.card_id, card.name}\n"
            else:
                deck_str += "  (Empty)\n"

        return deck_str

    def __len__(self):
        return len(self.cards)


def get_test_deck(deck_type: str = "goblin") -> Deck:
    test_deck = Deck()

    if deck_type == "goblin":
        gobs = find_card(minion_race="Goblin")
        for i in range(test_deck.card_limit):
            test_deck.add_card(gobs[random.randint(0, len(gobs) - 1)])

    elif deck_type == "gnome":
        gnomes = find_card(minion_race="Gnome")
        for i in range(test_deck.card_limit):
            test_deck.add_card(gnomes[random.randint(0, len(gnomes) - 1)])

    elif deck_type == "random":
        all_cards_list = get_all_cards()
        for i in range(test_deck.card_limit):
            test_deck.add_card(all_cards_list[random.randint(0, len(all_cards_list) - 1)])

    else:
        print('Invalid parameter. Try "goblin" or "gnome".')
        return

    return test_deck


def get_custom_deck():
    custom_deck = Deck()
    goblins = find_card(minion_race="Goblin")
    gnomes = find_card(minion_race="Gnome")

    for i in gnomes:
        custom_deck.add_card(i.card_id)
        custom_deck.add_card(i.card_id)

    for i in goblins:
        custom_deck.add_card(i.card_id)
        custom_deck.add_card(i.card_id)

    custom_deck.add_card("mdra000")
    custom_deck.add_card("mdra000")
    custom_deck.add_card("sfro000")
    custom_deck.add_card("sfro000")

    custom_deck.shuffle()

    return custom_deck


if __name__ == "__main__":
    # goblin_deck = get_test_deck("goblin")
    # gnome_deck = get_test_deck("goblin")
    # random_deck = get_test_deck("random")
    # print(random_deck)
    # goblin_deck.burn_deck()
    # goblin_deck.add_card("Dragonite3")
    # print(goblin_deck)
    # print(len(goblin_deck))
    # goblin_deck.burn_deck()
    # print(len(goblin_deck))
    # goblin_deck.add_card("asdf")
    # print(len(goblin_deck))
    # goblin_deck.add_card("Gnome")
    # goblin_deck.fill_with_card("Grandma Gnome", fill=-1.5)
    # goblin_deck.fill_with_card("Grandma Gnome", fill=0.5)
    # goblin_deck.fill_with_card(find_card("Grandma Gnome"), fill=9.9)
    # print(len(goblin_deck))
    # goblin_deck.remove_card(find_card("Grandma Gnome"))
    # print(goblin_deck)

    # _ = get_test_deck("gnome")
    # print(_)
    # print(len(_))
    # for i in range(10):
    #     _.remove_card(i)
    # print(len(_))
    # _.fill_with_card(find_card("sfro000"))
    # print(len(_))

    custom_deck = get_custom_deck()
    print(custom_deck)
