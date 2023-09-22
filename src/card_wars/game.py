from dataclasses import dataclass

from card_wars.board import Board


# TODO: Relocate methods from Board to GameSession
@dataclass
class GameSession:
    board: Board

    def draw_starting_cards(self):
        for player_num in [1, 2]:
            for _ in range(3):
                self.board.draw_card(player_num)


if __name__ == "__main__":
    pass
