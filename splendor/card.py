from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from config import NOBLE_SCORE
from tokens import Tokens


@dataclass
class Card(ABC):
    cost: Tokens = field(default_factory=Tokens)
    score: int = 0

    @abstractmethod
    def __repr__(self):
        pass


@dataclass
class Noble(Card):
    def __init__(self, cost: Tokens = None):
        if cost is None:
            cost = Tokens()  # Default to an empty Tokens object if no cost is provided
        super().__init__(cost=cost, score=NOBLE_SCORE)

    def __repr__(self):
        return f"Noble(score={self.score})"


@dataclass
class EvaluationCard(Card):
    level: int = 1
    bonus: Tokens = field(default_factory=Tokens)

    def __repr__(self):
        return (
            f"EvaluationCard(cost={self.cost.repr_non_zero()}, score={self.score}, "
            f"level={self.level}, bonus={self.bonus.repr_non_zero()})"
        )
