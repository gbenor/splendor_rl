import copy

import pytest
from board import Board
from card import Noble, EvaluationCard
from tokens import Tokens
from unittest.mock import MagicMock


def test_shuffle(mock_board):
    """Test shuffling the decks."""
    board = mock_board
    noble_deck_before = copy.deepcopy(board.noble_deck)
    eval_decks_before = [copy.deepcopy(deck) for deck in board.evaluation_decks]

    # Shuffle
    board.shuffle()

    # Ensure order changes in noble deck
    assert board.noble_deck != noble_deck_before

    # Ensure order changes in evaluation decks
    for deck, before in zip(board.evaluation_decks, eval_decks_before):
        assert deck != before


def test_start_new_board(mock_board):
    """Test starting a new board with exposed cards."""
    board = mock_board

    # Start the game with 3 players
    board.start_new_board(num_of_players=3)

    # Verify exposed evaluation cards
    for exposed, deck in zip(board.exposed_evaluation_cards, board.evaluation_decks):
        assert len(exposed) == 4
        for card in exposed:
            assert isinstance(card, EvaluationCard)

    # Verify exposed noble cards
    assert len(board.exposed_noble_cards) == 4
    for card in board.exposed_noble_cards:
        assert isinstance(card, Noble)


def test_take_evaluation_card(mock_board):
    """Test taking an evaluation card."""
    board = mock_board
    board.start_new_board(num_of_players=3)

    # Take a card from the first deck
    card = board.take_evaluation_card(deck_index=0, card_index=2)
    assert isinstance(card, EvaluationCard)

    # Verify the slot is replaced with a new card
    assert board.exposed_evaluation_cards[0][2] is not None
    assert isinstance(board.exposed_evaluation_cards[0][2], EvaluationCard)


def test_take_noble_card(mock_board):
    """Test taking a noble card."""
    board = mock_board
    board.start_new_board(num_of_players=3)

    # Take the first noble card
    card = board.take_noble_card(card_index=0)
    assert isinstance(card, Noble)

    # Verify the slot is set to None
    assert board.exposed_noble_cards[0] is None
