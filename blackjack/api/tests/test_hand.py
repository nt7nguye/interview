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
    "test_case, cards, is_blackjack",
    [
        (
            "ace 10 is blackjack",
            [1, 10],
            True,
        ),
        ("ace J is blackjack", [1, 11], True),
        ("2 cards not total 21 is not blackjack", [5, 10], False),
        (
            "3 cards total 21 is not blackjack",
            [12, 10, 1],
            False,
        ),
        (
            "3 cards total 21 is not blackjack",
            [5, 10, 6],
            False,
        ),
    ],
)
def test_hand_is_blackjack(test_case, cards, is_blackjack):
    hand = Hand([Card(suit=Suit.HEARTS, value=c) for c in cards], 0)
    assert hand.is_blackjack == is_blackjack, test_case


@pytest.mark.parametrize(
    "test_case, cards, can_split",
    [
        ("2 cards of same value can split", [1, 1], True),
        ("2 cards of different values cannot split", [1, 2], False),
    ],
)
def test_hand_can_split(test_case, cards, can_split):
    hand = Hand([Card(suit=Suit.HEARTS, value=c) for c in cards], 0)
    assert hand.can_split == can_split, test_case


@pytest.mark.parametrize(
    "test_case, cards, can_hit",
    [
        ("less than 21 hard can hit", [10, 7], True),
        ("less than 21 soft can hit", [1, 10, 7], True),
        ("cant hit on blackjack", [1, 10], False),
        ("cant hit on bust", [1, 13, 12], False),
        ("cant hit on 21", [6, 10, 5], False),
    ],
)
def test_hand_can_hit(test_case, cards, can_hit):
    hand = Hand([Card(suit=Suit.HEARTS, value=c) for c in cards], 0)
    assert hand.can_hit == can_hit, test_case


@pytest.mark.parametrize(
    "test_case, cards, can_double",
    [
        ("can double on 2 cards", [5, 10], True),
        ("cant double on 3 cards", [1, 10, 10], False),
        ("cant double on blackjack", [1, 10], False),
    ],
)
def test_hand_can_double(test_case, cards, can_double):
    hand = Hand([Card(suit=Suit.HEARTS, value=c) for c in cards], 0)
    assert hand.can_double == can_double, test_case


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


@pytest.mark.parametrize(
    "cards, expected_print",
    [
        ([2, 10], "2, 10 [12]"),
        ([1, 10], "A, 10 [11, 21]"),
        ([1, 1, 8], "A, A, 8 [10, 20, 30]"),
        ([1, 1, 1, 10], "A, A, A, 10 [13, 23, 33, 43]"),
    ],
)
def test_hand_print(cards, expected_print):
    hand = Hand([Card(suit=Suit.HEARTS, value=c) for c in cards], 0)
    assert str(hand) == expected_print, expected_print
