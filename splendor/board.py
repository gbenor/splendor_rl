from typing import List

from card import Noble, EvaluationCard
from deck import NobleDeck, EvaluationDeck
from tokens import Tokens


class Board:
    def __init__(self):
        self.noble_deck: NobleDeck = NobleDeck()
        self.evaluation_decks: List[EvaluationDeck] = [
            EvaluationDeck(i) for i in range(3)
        ]
        self.tokens = Tokens()  # Initialize tokens
        self.exposed_evaluation_cards: List[List[EvaluationCard]] = [
            [],
            [],
            [],
        ]  # 4 cards exposed for each deck
        self.exposed_noble_cards: List[Noble] = []

    def load_from_files(self, noble_file: str, evaluation_files: List[str]):
        # Load nobles
        self.noble_deck.read_from_csv(noble_file)

        # Load evaluation cards for each deck
        assert len(evaluation_files) == len(self.evaluation_decks)
        for i, eval_file in enumerate(evaluation_files):
            self.evaluation_decks[i].read_from_csv(eval_file)

    def shuffle(self):
        # Shuffle all decks
        self.noble_deck.shuffle()
        for deck in self.evaluation_decks:
            deck.shuffle()

    def start_new_board(self, num_of_players):
        # Reset and expose the top 4 cards of each evaluation deck
        self.exposed_evaluation_cards = [
            [deck.get_card() for _ in range(4)] for deck in self.evaluation_decks
        ]
        self.exposed_noble_cards = [
            self.noble_deck.get_card() for _ in range(num_of_players + 1)
        ]
        self.tokens = Tokens(
            red=7,
            green=7,
            blue=7,
            white=7,
            black=7,
            gold=5,
        )

    def take_evaluation_card(self, deck_index: int, card_index: int) -> EvaluationCard:
        # Take a card from the exposed cards of a specific deck
        card = self.exposed_evaluation_cards[deck_index][card_index]
        self.exposed_evaluation_cards[deck_index][card_index] = self.evaluation_decks[
            deck_index
        ].get_card()
        return card

    def take_noble_card(self, card_index: int) -> Noble:
        # Take a card from the exposed cards of a specific deck
        card = self.exposed_noble_cards[card_index]
        self.exposed_noble_cards[card_index] = None
        return card
