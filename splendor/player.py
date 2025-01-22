from typing import List

from board import Board
from card import Card, EvaluationCard, Noble
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

    def _bonuses(self) -> Tokens:
        return sum((deck.bonus for deck in self.evaluation_decks), Tokens())

    def _cost_after_bonus_usage(self, card: Card) -> Tokens:
        bonuses = self._bonuses()
        return Tokens(
            red=max(0, card.cost.red - bonuses.red),
            green=max(0, card.cost.green - bonuses.green),
            blue=max(0, card.cost.blue - bonuses.blue),
            white=max(0, card.cost.white - bonuses.white),
            black=max(0, card.cost.black - bonuses.black),
        )

    def _wildcard_to_use(self, cost: Tokens) -> int:
        remaining_cost = Tokens(
            red=max(0, cost.red - self.tokens.red),
            green=max(0, cost.green - self.tokens.green),
            blue=max(0, cost.blue - self.tokens.blue),
            white=max(0, cost.white - self.tokens.white),
            black=max(0, cost.black - self.tokens.black),
        )

        total_shortage = (
            remaining_cost.red
            + remaining_cost.green
            + remaining_cost.blue
            + remaining_cost.white
            + remaining_cost.black
        )
        return total_shortage

    def can_buy_evaluation_card(self, card: EvaluationCard) -> bool:
        """
        Check if the player can buy an evaluation card based on their tokens and bonuses.
        """
        # Calculate the cost after applying bonuses
        remaining_cost = self._cost_after_bonus_usage(card)
        gold_needed = self._wildcard_to_use(remaining_cost)
        return self.tokens.gold >= gold_needed

    def can_buy_noble_card(self, card: Noble) -> bool:
        """
        Check if the player can buy a Noble card based on their bonuses.
        """
        # Calculate the cost after applying bonuses
        remaining_cost = self._cost_after_bonus_usage(card)
        return remaining_cost == Tokens()
