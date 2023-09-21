from card_wars.card import *
from card_wars.import_cards import find_card
from card_wars.player import *

if __name__ == "__main__":
    war_axe = find_card("w00")
    goblin = find_card("m00")
    print(type(war_axe))

    player = Player()
    player.equip_weapon(war_axe)
    print(player)

    player.equip_weapon(war_axe)  # Can equip same weapon, this destroys old weapon
    player.equip_weapon(goblin)  # Cannot equip none-weapon type cards
