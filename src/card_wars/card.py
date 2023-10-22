from dataclasses import asdict, dataclass, field
from typing import List, Tuple

from card_wars.logs import logger

log = logger.info


@dataclass
class Card:
    card_id: str
    name: str
    description: str = ""
    card_text: str = ""
    mana_cost: int = 0


@dataclass
class Minion(Card):
    base_stats: Tuple[int, int, int] = (0, 0, 0)  # Attack, Health, Mana
    mod_stats: List[int] = field(default_factory=lambda: [0, 0, 0])
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

        # For modifying attack, health and mana
        self.mod_stats = [0, 0, 0]

    def take_damage(self, damage):
        #  Not sure if necessary to check divine shield and reborn in every take_damage.
        #  Maybe find better implementation. Should probably put active abilities in a separate attribute anyway.

        if "divine_shield" in self.ability and damage > 0:
            self.ability.remove("divine_shield")
            log(f"{self.name} lost Divine Shield.")
            return

        if damage > 0:
            self.health[0] -= damage
            if self.health[0] <= 0:
                log(f"{self.name} died while taking {damage} damage.")
            else:
                log(f"{self.name} took {damage} damage. Now at {self.health[0]} HP")

        if "reborn" in self.ability and self.health[0] <= 0:
            self.ability.remove("reborn")
            self.health = [1, self.base_stats[1]]
            log(f"{self.name} was reborn with [{self.attack}/{self.health[0]}]")

    def attack_target(self, target, attack_mod=0):
        atk_val = self.attack + attack_mod
        if atk_val <= 0:
            return

        if isinstance(target, Minion):
            attacking = f"{self.name} [{atk_val}/{self.health[0]}]"
            attacked = f"{target.name} [{target.attack}/{target.health[0]}]"
            log(f"{attacking} attacks {attacked}")

            target.take_damage(atk_val)
            self.take_damage(target.attack)

        else:
            target.take_damage(atk_val)
            log(f"{self.name} attacks {target.name} for {atk_val} damage.")

    def heal(self, value):
        old = self.health[0]
        new = min(old + value, self.health[1])
        self.health[0] = new
        log(f"{self.name} was healed for {new - old}.")

    def __add__(self, other):
        if not isinstance(other, Minion):
            raise ValueError("Can only merge with another Minion.")

        #  card_id is not super important, as the merged minions won't be stored
        new_id = f"{self.card_id}_{other.card_id}"

        #  name would be fun to implement a very lightweight language model TODO
        new_name = self.name[:3] + other.name[-3:]

        #  description is really w/e
        new_description = f"Amalgam"
        new_card_text = f"{self.card_text} {other.card_text}"

        # just join stats
        new_base_stats = tuple(x + y for x, y in zip(self.base_stats, other.base_stats))
        new_attack = self.attack + other.attack
        new_health = [x + y for x, y in zip(self.health, other.health)]

        #  Ok this entire thing below is ridankulous,
        #  but we need to check for empty strings...

        def is_empty(ability):
            return not ability or ability == "''"

        if is_empty(self.ability) and is_empty(other.ability):
            new_ability = ["''"]
        elif is_empty(self.ability):
            new_ability = other.ability.copy()
        elif is_empty(other.ability):
            new_ability = self.ability.copy()
        else:
            new_ability = self.ability.copy()
            new_ability.extend(other.ability)

        if "''" in new_ability and len(new_ability) > 1:
            new_ability.remove("''")

        #  We could probably solve this by checking for empty strings earlier.
        #  // End ridankulös

        #  TODO when both minions have abilities that can be merged,
        #  we should try to concat the effects of them

        new_battlecry = self.battlecry + other.battlecry
        new_deathrattle = self.deathrattle + other.deathrattle
        new_race = self.race if self.race == other.race else "Amalgam"

        return Minion(
            new_id,
            new_name,
            new_description,
            new_card_text,
            0,
            new_base_stats,
            [0, 0, 0],
            new_attack,
            new_health,
            new_ability,
            new_battlecry,
            new_deathrattle,
            new_race,
        )

    def __str__(self):
        str = f"{self.name} [{self.attack}/{self.health[0]}] Mana: {self.mana_cost}"
        if self.card_text != "":
            str += f"\n{self.card_text}"
        return str

    def __repr__(self):
        class_name = type(self).__name__
        attributes = asdict(self)
        return f"{class_name}({', '.join(f'{k}={v}' for k, v in attributes.items())})"


@dataclass
class Spell(Card):
    spell_type: str = "Default"
    target: int = 0
    damage: int = 0


@dataclass
class Weapon(Card):
    attack: int = 0
    durability: int = 0
    ability: str = None


if __name__ == "__main__":
    # Example card creation
    Foo = Minion(
        card_id="0", name="Foo", base_stats=[1, 2, 3], ability=["divine_shield"], race="Foo"
    )
    Bar = Minion(card_id="1", name="Bar", base_stats=[1, 2, 3], ability=["reborn"], race="Bar")

    # Merging minions
    FooBar = Foo + Bar

    # Example attack interaction
    Bar.attack_target(Foo)
    Foo.attack_target(Bar)
    Bar.attack_target(Foo)

    Foo.heal(100)
    Bar.heal(100)

    print(Foo)
    print(Bar)

    print(repr(FooBar))
