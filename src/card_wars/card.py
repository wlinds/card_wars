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
    max_health: int
    health: int = None
    race: str = None
    ability: List[dict] = field(default_factory=list)
    battlecry: List[dict] = field(default_factory=list)
    deathrattle: List[dict] = field(default_factory=list)

    def __post_init__(self):
        if self.health is None:
            self.health = self.max_health

    def take_damage(self, damage):
        if "divine_shield" in self.ability:
            self.ability.remove("divine_shield")
            log(f"{self.name} took no damage but lost divine shield.")
            return

        if damage > 0:
            self.health -= damage
            log(f"{self.name} took {damage} damage: [{self.attack}/{self.health}]")
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
        self.health = min(self.health + value, self.max_health)

    def __str__(self):
        str = (
            f"{self.name}: [{self.attack}/{self.health}] battlecry={self.battlecry}, {self.ability}"
        )
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
