import random
from dataclasses import dataclass, field
from typing import List, Optional

from card_wars.card import Card, Weapon
from card_wars.deck import Deck


@dataclass
class Player:
    name: str = f"P{random.randint(0,9)}"
    health: int = 30
    mana_bar: int = 0  # Total mana
    max_mana_bar: int = 10
    active_mana: int = 0  # Disposable mana
    deck: Deck = Deck()
    max_hand_size: int = 10
    hero_power: str = None
    weapon: Optional[Weapon] = None

    def __post_init__(self):
        # Format name
        self.name = self.name.strip()
        self.name = self.name.replace(".", "")
        self.name = self.name.replace(",", "")
        self.name = self.name.replace(" ", "_")

    def update_active_mana(self):
        """Should be called at the beginning of each turn."""
        self.active_mana = self.mana_bar

    def equip_weapon(self, weapon: Weapon):
        if isinstance(weapon, Weapon) and self.weapon != None:
            print(
                f"{self.name} already has {self.weapon.name} equipped. Old weapon has been destroyed and replaced by {weapon.name}."
            )
            self.weapon = weapon

        elif isinstance(weapon, Weapon) and self.weapon == None:
            print(f"{self.name} equipped {weapon.name}.")
            self.weapon = weapon

        else:
            print(f"Cannot equip {weapon}.")


if __name__ == "__main__":
    test_player = Player(name="Mr. Test     ")
    print(test_player.name, "hello")
