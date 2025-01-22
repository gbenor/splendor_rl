import csv
import random

import pytest

from board import Board
from card import EvaluationCard
from player import Player
from tokens import Tokens


@pytest.fixture
def random_csv_noble(tmp_path):
    """Fixture to create a random CSV file for NobleDeck."""
    file_path = tmp_path / "noble_deck.csv"
    with open(file_path, mode="w", newline="") as file:
        fieldnames = ["red", "green", "blue", "white", "black", "gold"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(10):  # Create 10 rows
            writer.writerow(
                {
                    "red": random.randint(0, 5),
                    "green": random.randint(0, 5),
                    "blue": random.randint(0, 5),
                    "white": random.randint(0, 5),
                    "black": random.randint(0, 5),
                    "gold": random.randint(0, 2),
                }
            )
    return file_path


@pytest.fixture
def random_csv_evaluation(tmp_path):
    """Fixture to create a random CSV file for EvaluationDeck."""
    file_path = tmp_path / "evaluation_deck.csv"
    with open(file_path, mode="w", newline="") as file:
        fieldnames = [
            "red",
            "green",
            "blue",
            "white",
            "black",
            "gold",
            "score",
            "bonus",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(15):  # Create 15 rows
            writer.writerow(
                {
                    "red": random.randint(0, 5),
                    "green": random.randint(0, 5),
                    "blue": random.randint(0, 5),
                    "white": random.randint(0, 5),
                    "black": random.randint(0, 5),
                    "gold": random.randint(0, 2),
                    "score": random.randint(1, 10),
                    "bonus": random.choice(
                        ["red", "green", "blue", "white", "black", "gold"]
                    ),
                }
            )
    return file_path


@pytest.fixture
def mock_board(random_csv_noble, random_csv_evaluation):
    """Fixture to create a mock Board instance."""
    board = Board()
    board.load_from_files(
        random_csv_noble,
        [random_csv_evaluation, random_csv_evaluation, random_csv_evaluation],
    )
    return board


@pytest.fixture
def player_with_tokens():
    """Fixture to create a player with tokens and bonuses."""
    player = Player()
    player.tokens = Tokens(red=2, green=3, blue=1, gold=2)  # Player tokens
    player.evaluation_decks[0].cards.append(
        EvaluationCard(
            cost=Tokens(),
            score=0,
            bonus=Tokens(red=1),
        )
    )
    player.evaluation_decks[1].cards.append(
        EvaluationCard(cost=Tokens(), score=0, bonus=Tokens(white=1))
    )

    return player


@pytest.fixture
def evaluation_card():
    """Fixture to create a sample evaluation card."""
    return EvaluationCard(
        cost=Tokens(red=3, green=3, blue=2, white=0, black=0),
        score=3,
        bonus=Tokens(blue=1),
    )
