from abc import ABC, abstractmethod
from typing import Type, List, Optional
import csv
import random

from card import Card, Noble, EvaluationCard
from tokens import Tokens


class Deck(ABC):
    def __init__(self):
        self.cards: List[Card] = []

    @staticmethod
    def _read_cost(row) -> Tokens:
        """Helper method to parse token costs from a CSV row."""
        return Tokens(
            red=int(row.get("red", 0)),
            green=int(row.get("green", 0)),
            blue=int(row.get("blue", 0)),
            white=int(row.get("white", 0)),
            black=int(row.get("black", 0)),
            gold=int(row.get("gold", 0)),
        )

    @staticmethod
    def _read_bonus(row) -> Tokens:
        """Helper method to parse bonus tokens from a CSV row."""
        bonus = row.get("bonus", None)
        if not bonus:
            raise ValueError("Bonus field is missing or empty in the row")
        return Tokens(
            red=int(bonus == "red"),
            green=int(bonus == "green"),
            blue=int(bonus == "blue"),
            white=int(bonus == "white"),
            black=int(bonus == "black"),
            gold=int(bonus == "gold"),
        )

    @staticmethod
    def _read_score(row) -> int:
        """Helper method to parse the score from a CSV row."""
        return int(row.get("score", 0))

    @abstractmethod
    def read_from_csv(self, file_path: str):
        """Abstract method to populate the deck from a CSV file."""
        pass

    def shuffle(self):
        """Shuffles the cards in the deck."""
        random.shuffle(self.cards)

    def get_card(self) -> Optional[Card]:
        """Removes and returns the top card from the deck."""
        return self.cards.pop() if self.cards else None

    @property
    def score(self) -> int:
        return sum(card.score for card in self.cards)


class NobleDeck(Deck):
    def __init__(self):
        super().__init__()

    def read_from_csv(self, file_path: str):
        """Populates the deck with Noble cards from a CSV file."""
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cost = Deck._read_cost(row)  # Use the static method from Deck
                self.cards.append(Noble(cost=cost))


class EvaluationDeck(Deck):
    def __init__(self, level: int):
        super().__init__()
        self.level = level

    def read_from_csv(self, file_path: str):
        """Populates the deck with EvaluationCard cards from a CSV file."""
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cost = Deck._read_cost(row)  # Use the static method from Deck
                score = Deck._read_score(row)
                bonus = Deck._read_bonus(row)
                self.cards.append(EvaluationCard(cost=cost, score=score, bonus=bonus, level=self.level))

    @property
    def bonus(self) -> Tokens:
        return sum((card.bonus for card in self.cards), Tokens())
