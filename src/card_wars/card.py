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


# ----- Spell logic ----- #

# This should probably be replaced by a more general function TODO: Add target


def cast_spell(player, card_id):
    """
    player: The player object to apply the spell to.
    player_num: 1 or 2 to indicate which player casts the spell.
    card_id: id of the spell
    """

    # Wild Growth
    if card_id == "s02":
        if player.mana_bar >= 0:
            player.mana_bar += 2  # TODO: Handle case when result is >10
            print(
                f"{player.name} cast 'Wild Growth' and increased their mana bar by 2. New mana: {player.mana_bar}"
            )
        else:
            print(f"{player.name} does not have enough mana to cast 'Wild Growth'.")


if __name__ == "__main__":
    boblin = Minion("id", "Goblin", "A small creature with a funky smell.", 1, 2, 2, "Goblin")
    print(boblin.name, " - ", boblin.description)

    fire_blast = Spell("id", "Fire Blast", "A burst of fire.", 2, "Fire", 0, 6)
    print(f"{fire_blast.mana_cost=}")

    small_shiv = Weapon("id", "Small Shiv", "Crafted from scraps.", 3, 3, 2)
