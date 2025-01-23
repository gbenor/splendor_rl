from typing import List

from board import Board
from config import SCORE_TO_WIN
from player import Player


class Game:
    def __init__(self):
        self.board: Board = None
        self.players: List[Player] = []
        self.max_rounds = None
        self.num_of_players = None
        self.rounds: int = 0
        self.current_player_id: int = 0

    def setup_game(
        self,
        noble_file: str,
        evaluation_files: List[str],
        num_of_players: int,
        max_rounds: int,
    ):
        self.board.load_from_files(
            noble_file,
            evaluation_files,
        )
        self.num_of_players = num_of_players
        self.max_rounds = max_rounds

    def start_new_game(self):
        self.rounds = 0
        self.current_player_id: int = 0
        self.board.shuffle()
        self.board.start_new_board(num_of_players=self.num_of_players)
        self.num_of_players = [Player() for _ in range(self.num_of_players)]

    def max_score(self):
        return max(player.score for player in self.players)

    @property
    def end(self) -> bool:
        return (
            self.max_score() >= SCORE_TO_WIN and self.current_player_id == 0
        ) or self.rounds > self.max_rounds

    def get_options_for_current_player_id(self):
        player = self.players[self.current_player_id]
        return {
            "withdrawal": player.get_withdrawal_options(self.board),
            "buy_evaluation": player.get_buy_evaluation_options(self.board),
            "buy_reserved": player.get_buy_reserved_options(),
            "reserved_without_gold": player.get_reserved_without_gold_options(
                self.board
            ),
            "reserved_with_gold": player.get_reserved_with_gold_options(self.board),
        }

    def finalize_turn(self):
        player = self.players[self.current_player_id]

        # for simplicity, but the first noble if possible
        noble_buying_options = player.noble_buying_options(self.board)
        if noble_buying_options:
            player.buy_noble_card(
                self.board,
                self.board.exposed_noble_cards.index(noble_buying_options[0]),
            )

        # advanced player id and num of turns
        if self.current_player_id == self.num_of_players - 1:
            self.rounds += 1
        self.current_player_id = (self.current_player_id + 1) % self.num_of_players
