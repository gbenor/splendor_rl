from typing import List

from board import Board
from deck import NobleDeck, EvaluationDeck
from tokens import Tokens


class Player:
    def __init__(self):
        self.noble_deck: NobleDeck = NobleDeck()
        self.evaluation_decks: List[EvaluationDeck] = [
            EvaluationDeck(i) for i in range(3)
        ]
        self.tokens = Tokens()  # Initialize tokens

    def get_withdrawal_options(self, board: Board) -> List[Tokens]:
        """
        Generate a list of all possible token withdrawal options from the main token deck
        on the board, based on the rules provided.
        """

        # withdraw noting is also an option
        options: List[Tokens] = [Tokens()]

        # Rule 1: Ensure no more than 10 tokens after withdrawal
        max_withdrawal = 10 - self.tokens.count
        if max_withdrawal <= 0:
            return options  # No options if the player already has 10 or more tokens

        # Rule 2: Withdraw 1, 2, or 3 tokens of different colors
        available_colors = [
            (color, getattr(board.tokens, color))
            for color in ["red", "green", "blue", "white", "black"]
            if getattr(board.tokens, color) > 0  # Exclude empty colors
        ]
        num_available_colors = len(available_colors)

        # Withdraw combinations of 1, 2, or 3 tokens (different colors)
        max_withdrawal_different_color = min(max_withdrawal, 3, num_available_colors)
        for i in range(1, max_withdrawal_different_color + 1):  # 1 to 3 tokens
            combinations = self._get_combinations(available_colors, i)
            for combo in combinations:
                options.append(Tokens(**{color: 1 for color, _ in combo}))

        # Rule 3: Withdraw 2 tokens of the same color (if there are at least 4 available)
        if max_withdrawal >= 2:
            for color in ["red", "green", "blue", "white", "black"]:
                if getattr(board.tokens, color) >= 4:
                    option = Tokens(**{color: 2})
                    options.append(option)

        return options

    @staticmethod
    def _get_combinations(colors, count):
        """Helper function to get combinations of colors."""
        from itertools import combinations

        return list(combinations(colors, count))
