from typing import List

from board import Board
from card import Card, EvaluationCard, Noble
from config import MAX_RESERVED_CARDS, MAX_TOKENS_PER_PLAYER
from deck import NobleDeck, EvaluationDeck
from tokens import Tokens


class Player:
    def __init__(self):
        self.noble_deck: NobleDeck = NobleDeck()
        self.evaluation_decks: List[EvaluationDeck] = [
            EvaluationDeck(i) for i in range(3)
        ]
        self.reserved_cards: List[EvaluationCard] = []
        self.tokens = Tokens()  # Initialize tokens

    def get_withdrawal_options(self, board: Board) -> List[Tokens]:
        """
        Generate a list of all possible token withdrawal options from the main token deck
        on the board, based on the rules provided.
        """

        # withdraw noting is also an option
        options: List[Tokens] = [Tokens()]

        # Rule 1: Ensure no more than 10 tokens after withdrawal
        max_withdrawal = MAX_TOKENS_PER_PLAYER - self.tokens.count
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

    def evaluation_buying_options(self, board) -> List[EvaluationCard]:
        options: List[EvaluationCard] = []
        for deck in board.exposed_evaluation_cards:
            for card in deck.cards:
                if self.can_buy_evaluation_card(card):
                    options.append(card)
        return options

    def noble_buying_options(self, board) -> List[Noble]:
        return [
            card for card in board.exposed_noble_cards if self.can_buy_noble_card(card)
        ]

    def can_buy_noble_card(self, card: Noble) -> bool:
        """
        Check if the player can buy a Noble card based on their bonuses.
        """
        # Calculate the cost after applying bonuses
        remaining_cost = self._cost_after_bonus_usage(card)
        return remaining_cost == Tokens()

    def buy_evaluation_card(self, board: Board, deck_index: int, card_index: int):
        # Validate deck and card indices
        if not (0 <= deck_index < len(board.exposed_evaluation_cards)) or not (
            0 <= card_index < len(board.exposed_evaluation_cards[deck_index])
        ):
            raise ValueError("Invalid deck_index or card_index.")
        card = board.exposed_evaluation_cards[deck_index][card_index]
        if not card:
            raise ValueError("No card at the specified index.")

        # Check if the player can afford the card
        if not self.can_buy_evaluation_card(card):
            raise ValueError("Player cannot afford the evaluation card.")

        # buy the card
        self._buy_card_helper(board, card)

        # Take the card and add it to the player's deck
        card = board.take_evaluation_card(deck_index, card_index)
        self.evaluation_decks[deck_index].cards.append(card)

    def buy_noble_card(self, board: Board, card_index: int):
        # Validate deck and card indices
        if not (0 <= card_index < len(board.exposed_noble_cards)):
            raise ValueError("Invalid card_index.")
        card = board.exposed_noble_cards[card_index]
        if not card:
            raise ValueError("No card at the specified index.")

        # Check if the player can afford the card
        if not self.can_buy_noble_card(card):
            raise ValueError("Player cannot afford the noble card.")

        card = board.take_noble_card(card_index)
        self.noble_deck.cards.append(card)

    def can_reserve(self):
        return len(self.reserved_cards) < MAX_RESERVED_CARDS

    def can_reserve_with_gold(self, board: Board):
        return (
            self.can_reserve()
            and board.tokens.gold > 0
            and self.tokens.count < MAX_TOKENS_PER_PLAYER
        )

    def reserve_without_gold(self, board: Board, deck_index: int, card_index: int):
        if not self.can_reserve():
            raise ValueError("Player cannot reserve a card.")
        card = board.take_evaluation_card(deck_index, card_index)
        self.reserved_cards.append(card)

    def reserve_with_gold(self, board: Board, deck_index: int, card_index: int):
        if not self.can_reserve_with_gold(board):
            raise ValueError("Player cannot reserve a card.")
        self.reserve_without_gold(board, deck_index, card_index)
        transaction = Tokens(
            gold=1,
        )

        self.tokens += transaction
        board.tokens -= transaction

    def buy_reserved_card(self, board: Board, card_index: int):
        # Validate deck and card indices
        if not (0 <= card_index < len(self.reserved_cards)):
            raise ValueError("Invalid deck_index or card_index.")
        card = self.reserved_cards[card_index]
        if not card:
            raise ValueError("No card at the specified index.")

        # Check if the player can afford the card
        if not self.can_buy_evaluation_card(card):
            raise ValueError("Player cannot afford the reserved card.")

        # buy the card
        self._buy_card_helper(board, card)

        # Take the card and add it to the player's deck
        card = self.reserved_cards.pop(card_index)
        self.evaluation_decks[card.level - 1].cards.append(card)

    def _buy_card_helper(self, board: Board, card: EvaluationCard):
        # Calculate remaining cost and the tokens to use
        remaining_cost = self._cost_after_bonus_usage(card)
        gold_needed = self._wildcard_to_use(remaining_cost)
        transaction = Tokens(
            red=min(remaining_cost.red, self.tokens.red),
            green=min(remaining_cost.green, self.tokens.green),
            blue=min(remaining_cost.blue, self.tokens.blue),
            white=min(remaining_cost.white, self.tokens.white),
            black=min(remaining_cost.black, self.tokens.black),
            gold=gold_needed,
        )

        # Deduct tokens from the player and return to the board
        self.tokens -= transaction
        board.tokens += transaction

    @property
    def score(self) -> int:
        return self.noble_deck.score + sum(deck for deck in self.evaluation_decks)

    def get_buy_evaluation_options(self, board: Board) -> List[EvaluationCard]:
        result: List[EvaluationCard] = []
        for deck in board.exposed_evaluation_cards:
            result.extend([card for card in deck if self.can_buy_evaluation_card(card)])
        return result

    def get_buy_reserved_options(self) -> List[EvaluationCard]:
        return [
            card for card in self.reserved_cards if self.can_buy_evaluation_card(card)
        ]

    def get_reserved_without_gold_options(self, board: Board) -> List[EvaluationCard]:
        if not self.can_reserve():
            return []

        result: List[EvaluationCard] = []
        for deck in board.exposed_evaluation_cards:
            result.extend([card for card in deck])
        return result

    def get_reserved_with_gold_options(self, board: Board) -> List[EvaluationCard]:
        if not self.can_reserve_with_gold(board):
            return []
        return self.get_reserved_without_gold_options(board)
