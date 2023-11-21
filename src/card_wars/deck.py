import copy
import json
import random
import string
from dataclasses import dataclass, field
from typing import List, Union

from card_wars.card import Card
from card_wars.import_cards import find_card, get_all_cards, read_cards_from


@dataclass
class Deck:
    name: str = "Default Deck"
    card_limit: int = 30
    cards: List[Card] = field(default_factory=list)
    copies_allowed: int = 30

    def __post_init__(self):
        if self.card_limit is None:
            self.card_limit = 9999

    def add_card(self, card: Union[str, Card]):
        """
        Add a copy of any card to deck card list.
        """

        # Find card if input is str (card_id or card_name)
        if isinstance(card, str):
            card = find_card(card)

        if card is None:
            return

        if sum(1 for c in self.cards if c.card_id == card.card_id) >= self.copies_allowed:
            print(f"{self.copies_allowed} copies of {card.name} already in the deck.")
            return

        if len(self.cards) >= self.card_limit:
            print(f"Deck is full ({self.card_limit} cards). Cannot add more cards.")
            return

        new_card = copy.deepcopy(card)
        self.cards.append(new_card)

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

        if cards_to_add < 0:
            print(f"Cannot add {cards_to_add} cards.")
            return

        for _ in range(cards_to_add):
            new_card = copy.deepcopy(card)  # TODO not sure if deepcopy is needed here
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

    def get_distribution(self):
        mana_cost = [card.mana_cost for card in self.cards]
        return mana_cost

    def __str__(self):
        header = f"{self.name} - [{len(self.cards)}/{self.card_limit}] cards:\n\n"

        card_counts = {}
        deck_str = ""
        for card in self.cards:
            if card.card_id in card_counts:
                card_counts[card.card_id] += 1
                deck_str += f"  {card_counts[card.card_id]}   {card.card_id}   {card.name}\n"
            else:
                card_counts[card.card_id] = 1
                deck_str += f"  1   {card.card_id}   {card.name}\n"

        return header + deck_str

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, i):
        return self.cards[i]


def get_test_deck(deck_type: str = "goblin") -> Deck:
    """
    Returns a deck in random order.

        Args:
            "goblin", "gnome", "random"
    """

    deck = Deck()

    if deck_type == "goblin":
        gobs = find_card(minion_race="Goblin")
        for i in range(deck.card_limit):
            deck.add_card(gobs[random.randint(0, len(gobs) - 1)])

    elif deck_type == "gnome":
        gnomes = find_card(minion_race="Gnome")
        for i in range(deck.card_limit):
            deck.add_card(gnomes[random.randint(0, len(gnomes) - 1)])

    elif deck_type == "random":
        all_cards_list = get_all_cards()
        for i in range(deck.card_limit):
            deck.add_card(all_cards_list[random.randint(0, len(all_cards_list) - 1)])

    else:
        print('Invalid parameter. Try "goblin" or "gnome".')
        return

    return deck


def get_custom_deck(card_list: Union[list, str], name: str = None, shuffled=False) -> Deck:
    """
    Constructs a custom deck from a list of card_ids or from a serialized string.
    """
    if isinstance(card_list, str):
        print("Converting serialized string to deck.")
        serializer = DeckSerializer()
        card_list = serializer.deserialize(card_list)
        if isinstance(card_list, list):  # Prevent recursion if serializer fails exception
            return get_custom_deck(card_list, name, shuffled)

    else:
        custom_deck = Deck()

        for card_id in card_list:
            custom_deck.add_card(card_id)

    if shuffled:
        custom_deck.shuffle()

    if custom_deck and name:
        custom_deck.name = name

    return custom_deck


class DeckSerializer:
    """
    Whenever a new card is added to the json pool,
    loading old decks with this WILL BREAK. # TODO

    """

    def __init__(self, deck=Deck()):
        self.deck = deck
        self.card_id = [card.card_id for card in get_all_cards()]
        self.mapping = self.generate_mapping(set(self.card_id))

    @staticmethod
    def generate_mapping(elements):
        code_length = 1
        mapping = {}

        # TODO This will only allow up to 62 unique cards, this can be improved by implementing combinations
        alphabet = string.ascii_letters + string.digits

        for i, element in enumerate(sorted(elements)):
            if i >= len(alphabet) ** code_length:
                code_length += 1
            code = "".join(
                alphabet[(i // len(alphabet) ** j) % len(alphabet)]
                for j in range(code_length - 1, -1, -1)
            )
            mapping[element] = code
        return mapping

    def serialize(self):
        return "".join(
            self.mapping[element] for element in [card.card_id for card in self.deck.cards]
        )

    def deserialize(self, short_string):
        reversed_mapping = {v: k for k, v in self.mapping.items()}
        try:
            return [
                reversed_mapping[short_string[i : i + 1]] for i in range(0, len(short_string), 1)
            ]
        except KeyError as e:
            print(f"Error: {e}. Input string is broken.")
            return []


if __name__ == "__main__":
    test_deck = get_test_deck("gnome")
    serializer = DeckSerializer(test_deck)

    shortened_string = serializer.serialize()
    print(shortened_string)

    deserialized = serializer.deserialize(shortened_string)
    print(deserialized)

    restored_deck = get_custom_deck(deserialized)
    print(restored_deck)

    deck = get_custom_deck("ddeeffgghhiijjkkllmmnnnnoobbsrr")
    # Yeah this formatting looks batshit crazy. #TODO

    mapping_dict = serializer.generate_mapping(serializer.mapping)
    print(mapping_dict.values())

    print(deck.get_distribution())
