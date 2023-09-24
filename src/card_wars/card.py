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

    def take_damage(self, damage):
        if damage > 0:
            self.health -= damage
            print(f"{self.name} took {damage} damage.")
        else:
            print(f"Invalid damage value: {damage}")


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
