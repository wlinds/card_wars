import random
from dataclasses import dataclass, field
from typing import List, Optional

from card_wars import logs
from card_wars.card import Card, Minion, Weapon
from card_wars.deck import Deck

log = logs.logger.info


@dataclass
class Player:
    name: str = f"P{random.randint(0,9)}"
    max_health: int = 30
    health: int = max_health
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

    def take_damage(self, damage):
        if damage > 0:
            self.health -= damage
            log(f"{self.name} takes {damage} damage. Current health: {self.health}")
        else:
            print(f"Invalid damage value: {damage}")

    def update_active_mana(self, n=None):
        """
        Should be called at the beginning of each turn.
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

        if isinstance(target, Player):
            log(
                f"{self.name} attacked {target.name} with {self.weapon.name} for {self.weapon.attack} damage."
            )
            target.take_damage(self.weapon.attack)

        elif isinstance(target, Minion):
            log(
                f"{self.name} attacked {target.name} [{target.attack}/{target.health}] with {self.weapon.name} for {self.weapon.attack} damage."
            )
            target.take_damage(self.weapon.attack)

        else:
            print("Invalid target.")

        self.weapon.durability -= 1

        if self.weapon.durability <= 0:
            log(f"{self.weapon.name} was destroyed.")
            self.weapon = None

    def heal(self, value):
        if value > 0:
            self.health += value
            if self.health > self.max_health:
                self.health = self.max_health  # Cap at max health
        else:
            print(f"Invalid heal value: {value}")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


if __name__ == "__main__":
    test_player = Player(name="Mr. Test     ")
    print(test_player.name, "hello")
