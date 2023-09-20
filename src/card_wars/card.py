from dataclasses import dataclass


@dataclass
class Card:
    card_id: str
    name: str
    description: str
    mana_cost: int


@dataclass
class Minion(Card):
    attack: int
    health: int
    race: str = None
    ability: str = None


@dataclass
class Spell(Card):
    spell_type: str
    target: int  # 0 = all entities, 1 = enemy entities, 2 = enemy minion only, 3 = player minion only, 4 = player character only etc (?)
    damage: int = 0


@dataclass
class Weapon(Card):
    attack: int
    durability: int


if __name__ == "__main__":
    boblin = Minion("Goblin", "A small creature with a funky smell.", 1, 2, 2, "Goblin")
    print(boblin.name, " - ", boblin.description)

    fire_blast = Spell("Fire Blast", "A burst of fire.", 2, "Fire", 0, 6)
    print(f"{fire_blast.mana_cost=}")

    small_shiv = Weapon("Small Shiv", "Crafted from scraps.", 3, 3, 2)
