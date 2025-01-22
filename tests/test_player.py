import pytest
from board import Board
from tokens import Tokens
from player import Player


@pytest.fixture
def setup_board():
    """Fixture to create a default board with tokens."""
    board = Board()
    board.tokens = Tokens(red=5, green=4, blue=3, white=2, black=1)
    return board


def test_withdraw_no_tokens_left(setup_board):
    """Test when the player already has 10 tokens."""
    board = setup_board
    player = Player()
    player.tokens = Tokens(
        red=2, green=2, blue=2, white=2, black=2
    )  # Player has 10 tokens

    options = player.get_withdrawal_options(board)
    assert options == [
        Tokens()
    ], "Player cannot withdraw tokens if they already have 10."


def test_withdraw_single_color_options(setup_board):
    """Test withdrawal options when the player can only withdraw single tokens."""
    board = setup_board
    player = Player()
    player.tokens = Tokens(red=1, green=1)  # Player has 2 tokens

    options = player.get_withdrawal_options(board)

    # Expected single-token withdrawals
    expected = [
        Tokens(red=1),
        Tokens(green=1),
        Tokens(blue=1),
        Tokens(white=1),
        Tokens(black=1),
    ]

    for option in expected:
        assert option in options, f"Expected withdrawal option {option} is missing."


def test_withdraw_two_tokens_of_same_color(setup_board):
    """Test withdrawal options when a player can withdraw 2 tokens of the same color."""
    board = setup_board
    player = Player()
    player.tokens = Tokens()  # Player starts with no tokens

    options = player.get_withdrawal_options(board)

    # Expected two-token withdrawal
    expected = [Tokens(red=2), Tokens(green=2)]

    for option in expected:
        assert (
            option in options
        ), f"Expected two-token withdrawal option {option} is missing."


def test_withdraw_three_different_tokens(setup_board):
    """Test withdrawal options for 3 different tokens."""
    board = setup_board
    player = Player()
    player.tokens = Tokens()  # Player starts with no tokens

    options = player.get_withdrawal_options(board)

    # Verify options for 3 different tokens
    three_token_options = [
        Tokens(red=1, green=1, blue=1),
        Tokens(red=1, green=1, white=1),
        Tokens(red=1, green=1, black=1),
        Tokens(green=1, blue=1, white=1),
        Tokens(green=1, blue=1, black=1),
        Tokens(blue=1, white=1, black=1),
    ]

    for option in three_token_options:
        assert (
            option in options
        ), f"Expected three-token withdrawal option {option} is missing."


def test_withdraw_mixed_options(setup_board):
    """Test a mix of all withdrawal options."""
    board = setup_board
    player = Player()
    player.tokens = Tokens(red=1, green=2)  # Player starts with 3 tokens

    options = player.get_withdrawal_options(board)

    # Verify that both single, two, and three token withdrawals are present
    expected = [
        Tokens(red=1),
        Tokens(green=1),
        Tokens(blue=1),
        Tokens(white=1),
        Tokens(black=1),
        Tokens(red=2),  # Two tokens of the same color
        Tokens(green=2),
        Tokens(red=1, green=1, blue=1),  # Three different colors
    ]

    for option in expected:
        assert option in options, f"Expected withdrawal option {option} is missing."
