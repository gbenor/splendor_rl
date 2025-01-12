from dataclasses import dataclass, field
from abc import ABC, abstractmethod

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
    def __init__(self):
        super().__init__(cost=Tokens(), score=3)

    def __repr__(self):
        return f"Noble(score={self.score})"


@dataclass
class EvaluationCard(Card):
    level: int = 1
    bonus: Tokens = field(default_factory=Tokens)

    def __repr__(self):
        return (f"EvaluationCard(cost={self.cost.repr_non_zero()}, score={self.score}, "
                f"level={self.level}, bonus={self.bonus.repr_non_zero()})")

