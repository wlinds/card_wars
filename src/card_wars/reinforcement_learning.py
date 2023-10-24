import os
import random

import numpy as np
import pandas as pd
from board import Board
from deck import *
from game import GameSession
from player import Player


def game_simulation(p1):
    # This is the deck p1 should win against (random goblin deck)
    p2 = Player(name="P2 Classic Deck", deck=get_test_deck())

    # Shuffle both deck for random order
    p1.deck.shuffle()
    p2.deck.shuffle()
    cw = GameSession(p1, p2, Board())
    cw.draw_starting_cards()
    cw.end_turn()

    while p1.health > 0 and p2.health > 0:
        cw.draw_card(1)
        cw.draw_card(2)

        # TODO better implementation of which card to play
        # TODO basic logic, also get hand length and evaluate cards in hand for play or not play

        get_active_mana = p1.active_mana
        cards_on_hand = cw.player1_hand
        if cards_on_hand != []:
            for card in cards_on_hand:
                #  TODO Implement card evaluation
                if card.mana_cost <= p1.active_mana:
                    idx = cards_on_hand.index(card)
                    cw.play_card(1, idx)

                #  TODO Optimize mana curve. Punish unspent mana. Reward well spent mana.

        get_active_mana = p2.active_mana
        cards_on_hand = cw.player2_hand
        if cards_on_hand != []:
            for card in cards_on_hand:
                # Implement card evaluation
                if card.mana_cost <= p2.active_mana:
                    idx = cards_on_hand.index(card)
                    cw.play_card(2, idx)

        if cw.player1.weapon != None:
            target = cw.target_assist(1, all_random=False, all_enemy=True)

            cw.player1.attack_target(random.choice(target))

        if cw.player2.weapon != None:
            target = cw.target_assist(2, all_random=False, all_enemy=True)
            cw.player2.attack_target(random.choice(target))

        cw.attack_phase()

    # print(cw)
    # print(cw.board)
    if p1.health > 0:
        return 1
    return 0


def reset_player(deck_string):
    deck = get_custom_deck(card_list=deck_string, name=deck_string)
    p1 = Player(name=deck_string, deck=deck)

    # p1 = Player(name="P1 Classic Deck", deck=get_test_deck())

    return p1


def get_available_cards():
    serializer = DeckSerializer()
    mapping_dict = serializer.generate_mapping(serializer.mapping)
    uids = list(set(mapping_dict.values()))
    uids_sorted = sorted(uids)

    return uids_sorted


def main(file_path):
    # Get an unsorted list of all available cards
    uid_bucket = get_available_cards()

    # Start out by randomly selecting any cards from the bucket
    deck = random.choices(uid_bucket, k=30)
    deck_string = "".join(deck)

    # deck = get_custom_deck(card_list=deck_string, deck_name=deck_string)

    # Testing with same goblin bucket to ensure simulation is fair
    deck = get_test_deck()  # Hypothetically this should be 50/50 w/l

    # Number of generations for later
    num_generations = 1

    # Save deck_uid (we will also store deck performance in this df)
    # We will store card values as we go on, for now it's just one bool
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)

        respose = input(f"File {file_path} already exist. Continue writing to it? [Y/N] ")
        if respose.lower() != "y" and respose.lower() != "yes":
            print("Aborted")
            return
    else:
        df = pd.DataFrame(columns=["generation", "deck_uid", "win_rate"])

    for generation in range(num_generations):
        for _ in range(2):
            # Full random start:
            deck_string = "".join(random.choices(uid_bucket, k=30))

            # Test with same deck as P2
            # serializer = DeckSerializer(get_test_deck())
            # deck_string = serializer.serialize()
            # Also running an instance every loop is not computtional healthy...

            p1 = reset_player(deck_string)

            win_rate_sum = 0

            for _ in range(10):
                result = game_simulation(p1)
                win_rate_sum += result
                p1 = reset_player(deck_string)

            df = df._append(
                {"generation": generation, "deck_uid": deck_string, "win_rate": win_rate_sum},
                ignore_index=True,
            )

    df.to_csv(file_path, index=False)

    return df


if __name__ == "__main__":
    df = main(file_path="data/results/goblin_vs_random_2_allow_player_attack.csv")
    print(df)
    print(df["win_rate"].mean())
    print("Top 5 best performing deck:")
    top_5_decks = df.nlargest(5, "win_rate")
    print(top_5_decks)
