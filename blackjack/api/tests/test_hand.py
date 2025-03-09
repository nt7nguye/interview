from blackjack.api.core.card import Suit
from core import Card, Hand
import pytest


@pytest.mark.parametrize(
    "test_case, cards, is_bust",
    [
        (
            "no aces and not bust",
            [12, 10],
            False,
        ),
        (
            "no aces and bust (22)",
            [13, 10, 2],
            True,
        ),
        (
            "one ace and not bust (13, 23)",
            [1, 10, 2],
            False,
        ),
        (
            "one ace and bust (23)",
            [1, 13, 12, 2],
            True,
        ),
    ],
)
def test_hand_is_bust(test_case, cards, is_bust):
    hand = Hand([Card(suit=Suit.HEARTS, value=c) for c in cards], 0)
    assert hand.is_bust == is_bust, test_case


@pytest.mark.parametrize(
    "test_case, cards, expected_values",
    [
        (
            "no aces",
            [2, 10],
            [12],
        ),
        (
            "one ace",
            [1, 10],
            [11, 21],
        ),
        (
            "two aces",
            [1, 1],
            [2, 12, 22],
        ),
        (
            "two aces and an 8",
            [1, 1, 8],
            [10, 20, 30],
        ),
        (
            "three aces and a 10",
            [1, 1, 1, 10],
            [13, 23, 33, 43],
        ),
    ],
)
def test_hand_possible_values(test_case, cards, expected_values):
    hand = Hand([Card(suit=Suit.HEARTS, value=c) for c in cards], 0)
    assert hand.possible_values == expected_values, test_case
