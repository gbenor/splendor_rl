from typing import List, Dict, Union, Any
from board import Board
from card import EvaluationCard
from config import SCORE_TO_WIN
from player import Player
from tokens import Tokens


class Game:
    def __init__(self):
        self.board: Board = Board()
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
        self.players = [Player() for _ in range(self.num_of_players)]

    def max_score(self):
        return max(player.score for player in self.players)

    @property
    def end(self) -> bool:
        return (
            self.max_score() >= SCORE_TO_WIN and self.current_player_id == 0
        ) or self.rounds > self.max_rounds

    def get_options_for_current_player_id(
        self,
    ) -> Dict[str, List[Union[Tokens, EvaluationCard]]]:
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

    def apply_option(
        self, option: Dict[str, Any], option_dict: Dict[str, List[Any]]
    ) -> bool:
        player = self.players[self.current_player_id]

        # Validate input
        if len(option) != 1:
            raise ValueError("Option must contain exactly one operation.")
        if not isinstance(option_dict, dict):
            raise ValueError("option_dict must be a dictionary.")

        # Extract operation and data
        operation, data = next(iter(option.items()))

        # Check if the operation is valid
        if operation not in option_dict or data not in option_dict[operation]:
            return False

        # Operation handlers
        if operation == "withdrawal":
            player.withdrawal(self.board, data)
            return True

        if operation == "buy_evaluation":
            return self._apply_buy_evaluation(player, data)

        if operation == "buy_reserved":
            return self._apply_buy_reserved(player, data)

        if operation == "reserved_without_gold":
            return self._apply_reserve_without_gold(player, data)

        if operation == "reserved_with_gold":
            return self._apply_reserve_with_gold(player, data)

        # Unknown operation
        raise ValueError(f"Unknown operation: {operation}")

    # Helper Methods
    def _apply_buy_evaluation(self, player, data):
        """Handle 'buy_evaluation' operation."""
        for deck_index, card_list in enumerate(self.board.exposed_evaluation_cards):
            if data in card_list:
                player.buy_evaluation_card(
                    self.board, deck_index, card_list.index(data)
                )
                return True
        return False

    def _apply_buy_reserved(self, player, data):
        """Handle 'buy_reserved' operation."""
        if data in player.reserved_cards:
            player.buy_reserved_card(self.board, player.reserved_cards.index(data))
            return True
        return False

    def _apply_reserve_without_gold(self, player, data):
        """Handle 'reserved_without_gold' operation."""
        for deck_index, card_list in enumerate(self.board.exposed_evaluation_cards):
            if data in card_list:
                player.reserve_without_gold(
                    self.board, deck_index, card_list.index(data)
                )
                return True
        return False

    def _apply_reserve_with_gold(self, player, data):
        """Handle 'reserved_with_gold' operation."""
        for deck_index, card_list in enumerate(self.board.exposed_evaluation_cards):
            if data in card_list:
                player.reserve_with_gold(self.board, deck_index, card_list.index(data))
                return True
        return False

    def _buying_noble(self):
        player = self.players[self.current_player_id]
        noble_buying_options = player.noble_buying_options(self.board)
        if noble_buying_options:
            player.buy_noble_card(
                self.board,
                self.board.exposed_noble_cards.index(noble_buying_options[0]),
            )

    def finalize_turn(self):
        # Handle noble purchase if possible
        self._buying_noble()

        # Advance player turn and rounds
        if self.current_player_id == self.num_of_players - 1:
            self.rounds += 1
        self.current_player_id = (self.current_player_id + 1) % self.num_of_players

    @property
    def rounds(self) -> int:
        return self.rounds

    @property
    def player_id(self) -> int:
        return self.current_player_id
