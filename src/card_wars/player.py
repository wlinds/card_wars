import random
from dataclasses import dataclass, field
from typing import List, Optional

from card_wars import logs
from card_wars.card import Card, Minion, Spell, Weapon
from card_wars.deck import Deck, get_test_deck

log = logs.logger.info

# Overloads default list to always get the first index (current health)
# class HealthValue(list):
#     def __gt__(self, other):
#         return self[0] > other

#     def __lt__(self, other):
#         return self[0] < other

#     def __eq__(self, other):
#         return self[0] == other

#     def __add__(self, other):
#         return self[0] + other

#     def __sub__(self, other):
#         return self[0] - other

#     def __getitem__(self, key):
#         return super().__getitem__(0) if key == 0 else super().__getitem__(key)

#     def __setitem__(self, key, value):
#         if key == 0:
#             super().__setitem__(0, value)
#         else:
#             super().__setitem__(key, value)


@dataclass
class Player(Minion):
    name: str = f"P{random.randint(0,9)}"
    max_health: int = 30
    mana_bar: int = 0  # Total mana
    max_mana_bar: int = 10
    active_mana: int = 0  # Disposable mana
    deck: Deck = Deck()
    hero_power: str = None
    weapon: Optional[Weapon] = None

    max_hand_size: int = 10
    hand: List[Card] = field(default_factory=list)
    overdraw_damage: int = 0

    def __post_init__(self):  # Format name
        self.name = self.name.strip().replace(".", "").replace(",", "").replace(" ", "_")
        self.health[0], self.health[1] = (
            self.max_health,
            self.max_health,
        )  # Probably not necessary, just update default

    def get_hand(self):
        return [i.name for i in self.hand]

    def draw_card(self):
        """
        Draw a card from deck and add it to hand.
        """

        if not self.deck.cards:
            log(f"{self.name} attempted do draw a card but has no cards left in their deck!")
            self.take_damage(self.overdraw_damage)
            self.overdraw_damage += 1
            return

        drawn_card = self.deck.draw_card()

        if isinstance(drawn_card, Minion):
            log(
                f"{self.name} drew: {drawn_card.name} [{drawn_card.attack}/{drawn_card.health[0]}] Mana cost: {drawn_card.mana_cost}"
            )
        elif isinstance(drawn_card, Spell) or isinstance(drawn_card, Weapon):
            log(f"{self.name} drew: {drawn_card.name} Mana cost: {drawn_card.mana_cost}")

        else:
            log(f"{self.player.name} drew {drawn_card}")

        self.add_to_hand(drawn_card)

    def add_to_hand(self, card):
        """Add a copy of any card to player hand."""
        if card is not None and len(self.hand) < self.max_hand_size:
            self.hand.append(card)
        else:
            log(f"Hand full! {card} was discarded.")

    def update_active_mana(self, n=None):
        """
        Called at the beginning of each turn.
        Can also be called to update with any n.
        """
        if n is not None:
            self.active_mana = n
        else:
            self.active_mana = self.mana_bar

    def equip_weapon(self, weapon: Weapon):
        if isinstance(weapon, Weapon) and self.weapon != None:
            log(
                f"{self.name} already has {self.weapon.name} equipped. Old weapon has been destroyed and replaced by {weapon.name}."
            )
            self.weapon = weapon

        elif isinstance(weapon, Weapon) and self.weapon == None:
            log(f"{self.name} equipped {weapon.name} [{weapon.attack}/{weapon.durability}].")
            self.weapon = weapon

        else:
            print(f"Cannot equip {weapon}.")

    # This could probably also be inherited from Minion..
    def attack_target(self, target):
        """
        Attacks with player weapon. Returns none.
        """

        if self.weapon is None:
            print("Cannot attack with no equipped weapon.")
            return

        if self.weapon.attack <= 0:
            print("Cannot attack with 0 attack weapon.")
            return

        # This should be merged, no need to handle Player/Minion instances differently
        if isinstance(target, Player):
            log(
                f"{self.name} attacked {target.name} with {self.weapon.name} for {self.weapon.attack} damage."
            )
            target.take_damage(self.weapon.attack)

        elif isinstance(target, Minion):
            log(
                f"{self.name} attacked {target.name} [{target.attack}/{target.health[0]}] with {self.weapon.name} for {self.weapon.attack} damage."
            )
            target.take_damage(self.weapon.attack)

        else:
            print("Invalid target.")

        self.weapon.durability -= 1

        if self.weapon.durability <= 0:
            log(f"{self.weapon.name} was destroyed.")
            self.weapon = None

    def __str__(self):
        return self.name

    def __repr__(self):
        class_name = type(self).__name__
        attributes = [f"{attr}={getattr(self, attr)}" for attr in self.__annotations__.keys()]
        return f"{class_name}({', '.join(attributes)})"


if __name__ == "__main__":
    p1 = Player()
    p2 = Player()
    p1.deck = get_test_deck()
    print(repr(p1))
    p1.take_damage(3)
    p1.heal(5)
    p1.attack_target(p2)
