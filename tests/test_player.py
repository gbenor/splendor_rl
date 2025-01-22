import pytest
from board import Board
from card import Noble
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


def test_can_buy_with_sufficient_tokens_and_bonuses(
    player_with_tokens, evaluation_card
):
    """Test if the player can buy a card when they have sufficient tokens and bonuses."""
    player = player_with_tokens
    card = evaluation_card

    # Player has enough tokens and bonuses to buy the card
    assert player.can_buy_evaluation_card(card) is True


def test_cannot_buy_due_to_insufficient_tokens(player_with_tokens, evaluation_card):
    """Test if the player cannot buy a card due to insufficient tokens."""
    player = player_with_tokens
    card = evaluation_card

    # Reduce player's tokens to make them insufficient
    player.tokens = Tokens(red=1, green=1, blue=0, gold=0)

    assert player.can_buy_evaluation_card(card) is False


def test_can_buy_with_wildcards(player_with_tokens, evaluation_card):
    """Test if the player can buy a card using wildcards (gold tokens)."""
    player = player_with_tokens
    card = evaluation_card

    # Player has 2 gold tokens to cover any shortages
    player.tokens = Tokens(red=1, green=2, blue=0, gold=4)

    assert player.can_buy_evaluation_card(card) is True


def test_cannot_buy_when_short_on_gold(player_with_tokens, evaluation_card):
    """Test if the player cannot buy a card when they don't have enough wildcards (gold)."""
    player = player_with_tokens
    card = evaluation_card

    # Player has a shortage but only 1 gold token
    player.tokens = Tokens(red=1, green=2, blue=0, gold=1)

    assert player.can_buy_evaluation_card(card) is False


def test_can_buy_with_exact_tokens_and_bonuses(player_with_tokens, evaluation_card):
    """Test if the player can buy a card with exactly enough tokens and bonuses."""
    player = player_with_tokens
    card = evaluation_card

    # Adjust tokens and bonuses to exactly match the cost
    player.tokens = Tokens(red=2, green=3, blue=2, gold=0)

    assert player.can_buy_evaluation_card(card) is True


def test_can_buy_noble(player_with_tokens):
    """Test if the player can buy a card with exactly enough tokens and bonuses."""
    player = player_with_tokens
    noble = Noble(cost=Tokens(red=1))
    assert player.can_buy_noble_card(noble) is True


def test_cant_buy_noble(player_with_tokens):
    """Test if the player can buy a card with exactly enough tokens and bonuses."""
    player = player_with_tokens
    noble = Noble(cost=Tokens(blue=1))
    assert player.can_buy_noble_card(noble) is False


def test_reserve_card_without_gold(mock_board, player_with_tokens):
    """Test reserving a card without using gold."""
    board = mock_board
    player = player_with_tokens

    # Reserve a card from deck 0 without gold
    player.reserve_without_gold(board, deck_index=0, card_index=0)

    # Assert that the card is now in the player's reserved cards
    assert len(player.reserved_cards) == 1
    assert player.reserved_cards[0] == board.exposed_evaluation_cards[0][0]

    # Assert the card is removed from the board
    assert board.exposed_evaluation_cards[0][0] is None


def test_reserve_card_with_gold(mock_board, player_with_tokens):
    """Test reserving a card and receiving a gold token."""
    board = setup_board
    player = setup_player

    # Reserve a card from deck 1 with gold
    player.reserve_with_gold(board, deck_index=1, card_index=1)

    # Assert that the card is now in the player's reserved cards
    assert len(player.reserved_cards) == 1
    assert player.reserved_cards[0] == board.exposed_evaluation_cards[1][1]

    # Assert the card is removed from the board
    assert board.exposed_evaluation_cards[1][1] is None

    # Assert the player received a gold token
    assert player.tokens.gold == 3
    assert board.tokens.gold == 2


#
# def test_buy_reserved_card_success(setup_board, setup_player):
#     """Test buying a reserved card successfully."""
#     board = setup_board
#     player = setup_player
#
#     # Reserve a card
#     player.reserve_with_gold(board, deck_index=0, card_index=0)
#
#     # Buy the reserved card
#     player.buy_reserved_card(board, card_index=0)
#
#     # Assert the reserved card is removed from the player's reserved cards
#     assert len(player.reserved_cards) == 0
#
#     # Assert the card is added to the player's evaluation deck
#     assert len(player.evaluation_decks[0].cards) == 1
#     assert player.evaluation_decks[0].cards[0].cost == Tokens(red=2, green=2, blue=0)
#
#     # Assert tokens were deducted correctly
#     assert player.tokens.red == 1  # Player initially had 3 red tokens
#     assert player.tokens.green == 1  # Player initially had 3 green tokens
#     assert player.tokens.blue == 1  # Player initially had 1 blue token
#     assert player.tokens.gold == 2  # Gold token usage should be validated
#
#
# def test_buy_reserved_card_insufficient_tokens(setup_board, setup_player):
#     """Test buying a reserved card fails when the player doesn't have enough tokens."""
#     board = setup_board
#     player = setup_player
#
#     # Reserve a card
#     player.reserve_with_gold(board, deck_index=1, card_index=1)
#
#     # Modify player's tokens to make the purchase impossible
#     player.tokens = Tokens(red=1, green=1, blue=0, gold=0)
#
#     with pytest.raises(ValueError, match="Player cannot afford the evaluation card."):
#         player.buy_reserved_card(board, card_index=0)
#
#
# def test_buy_reserved_card_invalid_index(setup_board, setup_player):
#     """Test buying a reserved card fails with an invalid index."""
#     board = setup_board
#     player = setup_player
#
#     # Reserve a card
#     player.reserve_with_gold(board, deck_index=0, card_index=0)
#
#     # Try buying a card with an invalid index
#     with pytest.raises(ValueError, match="Invalid deck_index or card_index."):
#         player.buy_reserved_card(board, card_index=1)
