from dataclasses import dataclass, field
from typing import List

from card_wars.logs import logger

log = logger.info


@dataclass
class Card:
    card_id: str
    name: str
    description: str
    mana_cost: int
    card_text: str


@dataclass
class Minion(Card):
    attack: int
    health: int
    race: str = None
    ability: str = None
    buffs: List[str] = field(default_factory=list)

    def take_damage(self, damage):
        if "divine_shield" in self.buffs:
            self.buffs.remove("divine_shield")
            log(f"{self.name} took no damage but lost divine shield.")
            return

        if damage > 0:
            self.health -= damage
            log(f"{self.name} took {damage} damage.")
        else:
            print(f"Invalid damage value: {damage}")

    def attack_target(self, target):
        if self.attack <= 0:
            print(f"Cannot attack with {self.name} (attack value <= 0).")
            return

        elif isinstance(target, Minion):
            log(
                f"{self.name} [{self.attack}/{self.health}] attacks {target.name} [{target.attack}/{target.health}] for {self.attack} damage."
            )
            target.take_damage(self.attack)
            self.take_damage(target.attack)
        else:
            target.take_damage(self.attack)
            log(f"{self.name} attacked {target.name} for {self.attack} damage.")

    def heal(self, value):
        # TODO prevent going over max health, probably add another max_health attribute
        self.health += value

    def __str__(self):
        str = f"{self.name}: [{self.attack}/{self.health}] Buffs={self.buffs}"
        return str


@dataclass
class Spell(Card):
    spell_type: str
    target: int  # 0 = all entities, 1 = enemy entities, 2 = enemy minion only, 3 = player minion only, 4 = player character only etc (?)
    damage: int = 0


@dataclass
class Weapon(Card):
    attack: int
    durability: int
    ability: str = None
