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


# ----- Spell logic ----- #

# This should probably be replaced by a more general function TODO: Add target


def cast_spell(player, card_id):
    """
    player: The player object to apply the spell to.
    player_num: 1 or 2 to indicate which player casts the spell.
    card_id: id of the spell
    """

    # Wild Growth
    if card_id == "snat000":
        if player.mana_bar >= 0:
            player.mana_bar += 2  # TODO: Handle case when result is >10
            print(
                f"{player.name} cast 'Wild Growth' and increased their mana bar by 2. New mana: {player.mana_bar}"
            )
        else:
            print(f"{player.name} does not have enough mana to cast 'Wild Growth'.")
