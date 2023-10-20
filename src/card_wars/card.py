from dataclasses import dataclass, field
from typing import List, Tuple

from card_wars.logs import logger

log = logger.info


@dataclass
class Card:
    card_id: str
    name: str
    description: str
    card_text: str
    mana_cost: int = 0


@dataclass
class Minion(Card):
    base_stats: Tuple[int, int, int] = (0, 0, 0)
    attack: int = 0
    health: List[int] = field(default_factory=lambda: [0, 0])
    ability: List[dict] = field(default_factory=list)
    battlecry: List[dict] = field(default_factory=list)
    deathrattle: List[dict] = field(default_factory=list)
    race: str = None

    def __post_init__(self):
        self.attack = self.base_stats[0]
        self.health[0] = self.base_stats[1]  # Current health
        self.health[1] = self.base_stats[1]  # Max health
        self.mana_cost = self.base_stats[2]

    def get_minion_attack_value(self):
        # TODO Check board buffs:
        # For example "When a friendly Goblin attacks, give it +3 attack"
        buff_value = 0

        return self.attack + buff_value

    def take_damage(self, damage):
        # // keep this check here until more damage affecting abilities added

        if "divine_shield" in self.ability and damage > 0:
            self.ability.remove("divine_shield")
            log(f"{self.name} lost Divine Shield.")
            return

        ## //

        if damage > 0:
            self.health[0] -= damage
            log(f"{self.name} took {damage} damage: [{self.attack}/{self.health[0]}]")
        else:
            print(f"Invalid damage value: {damage}")

    def attack_target(self, target):
        if self.attack <= 0:
            print(f"{self.name} cannot attack with {self.attack=}")
            return

        elif isinstance(target, Minion):
            log(
                f"{self.name} [{self.get_minion_attack_value()}/{self.health[0]}] attacks {target.name} [{target.attack}/{target.health[0]}] for {self.get_minion_attack_value()} damage."
            )

            target.take_damage(self.get_minion_attack_value())
            self.take_damage(target.get_minion_attack_value())
        else:
            target.take_damage(self.get_minion_attack_value())
            log(f"{self.name} attacked {target.name} for {self.attack} damage.")

    def heal(self, value):
        self.health[0] = min(self.health[0] + value, self.health[1])

    def __str__(self):
        str = f"[{self.attack}/{self.health[0]}] Mana: {self.mana_cost}\n{self.card_text}"
        return str


@dataclass
class Spell(Card):
    spell_type: str = "Default"
    target: int = 0  # 0 = all entities, 1 = enemy entities, 2 = enemy minion only, 3 = player minion only, 4 = player character only etc (?)
    damage: int = 0


@dataclass
class Weapon(Card):
    attack: int = 0
    durability: int = 0
    ability: str = None
