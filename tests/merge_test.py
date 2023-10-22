from card_wars.card import Minion
from card_wars.import_cards import find_card


def main():
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

    Belsebub = find_card("Belsebub")

    print(repr(Belsebub))
    print(repr(FooBar))

    result = FooBar + Belsebub
    print(repr(result))
    print(result.name)


if __name__ == "__main__":
    main()
