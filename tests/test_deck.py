import pytest
import csv
import random
from deck import NobleDeck, EvaluationDeck
from tokens import Tokens
from card import Noble, EvaluationCard


@pytest.fixture
def random_csv_noble(tmp_path):
    """Fixture to create a random CSV file for NobleDeck."""
    file_path = tmp_path / "noble_deck.csv"
    with open(file_path, mode="w", newline="") as file:
        fieldnames = ["red", "green", "blue", "white", "black", "gold"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(10):  # Create 10 rows
            writer.writerow({
                "red": random.randint(0, 5),
                "green": random.randint(0, 5),
                "blue": random.randint(0, 5),
                "white": random.randint(0, 5),
                "black": random.randint(0, 5),
                "gold": random.randint(0, 2),
            })
    return file_path


@pytest.fixture
def random_csv_evaluation(tmp_path):
    """Fixture to create a random CSV file for EvaluationDeck."""
    file_path = tmp_path / "evaluation_deck.csv"
    with open(file_path, mode="w", newline="") as file:
        fieldnames = ["red", "green", "blue", "white", "black", "gold", "score", "bonus"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(15):  # Create 15 rows
            writer.writerow({
                "red": random.randint(0, 5),
                "green": random.randint(0, 5),
                "blue": random.randint(0, 5),
                "white": random.randint(0, 5),
                "black": random.randint(0, 5),
                "gold": random.randint(0, 2),
                "score": random.randint(1, 10),
                "bonus": random.choice(["red", "green", "blue", "white", "black", "gold"]),
            })
    return file_path


def test_noble_deck(random_csv_noble):
    """Test NobleDeck functionality."""
    noble_deck = NobleDeck()
    noble_deck.read_from_csv(random_csv_noble)

    # Verify the correct number of cards
    assert len(noble_deck.cards) == 10

    # Verify all cards are instances of Noble
    assert all(isinstance(card, Noble) for card in noble_deck.cards)

    # Shuffle and get a card
    noble_deck.shuffle()
    card = noble_deck.get_card()
    assert isinstance(card, Noble)
    assert len(noble_deck.cards) == 9  # One card removed
    assert noble_deck.score == 3 * len(noble_deck.cards)


def test_evaluation_deck(random_csv_evaluation):
    """Test EvaluationDeck functionality."""
    evaluation_deck = EvaluationDeck(level=2)
    evaluation_deck.read_from_csv(random_csv_evaluation)

    # Verify the correct number of cards
    assert len(evaluation_deck.cards) == 15

    # Verify all cards are instances of EvaluationCard
    assert all(isinstance(card, EvaluationCard) for card in evaluation_deck.cards)

    # Verify card attributes
    for card in evaluation_deck.cards:
        assert card.score > 0
        assert isinstance(card.bonus, Tokens)

    # Shuffle and get a card
    evaluation_deck.shuffle()
    card = evaluation_deck.get_card()
    assert isinstance(card, EvaluationCard)
    assert len(evaluation_deck.cards) == 14  # One card removed

    bonus_dict = Tokens().__dict__.copy()  # Start with a clean copy of an empty Tokens object
    for card in evaluation_deck.cards:
        for key, value in card.bonus.__dict__.items():
            bonus_dict[key] += value  # Sum values for duplicate keys

    assert evaluation_deck.bonus.__dict__ == bonus_dict
