from re import I
from blackjack.api.core.card import Card, Suit
from blackjack.api.core.hand import Hand
import pytest
from core import BlackjackGame, Action


@pytest.fixture(scope="function")
def game():
    return BlackjackGame(num_decks=1)


def test_game_initialization(game):
    assert game.num_decks == 1
    assert len(game.deck.cards) == 52


def test_start_round(game):
    player_information = game.start_round(bet_size=10)

    # User have 1 hand, 2 cards, bet 10
    assert len(player_information.current_game.player_hands) == 1
    assert len(player_information.current_game.player_hands[0].cards) == 2
    assert player_information.current_game.player_hands[0].bet_amount == 10

    # Dealer has 1 card (the other one hidden)
    assert len(player_information.current_game.dealer_hand.cards) == 1
    assert len(game.dealer_hand.cards) == 2

    # Game history
    assert len(player_information.game_history) == 0


def test_multiple_rounds_eventually_shuffle(game):
    game.start_round(bet_size=10)
    game.apply_action(Action.STAND)

    shuffle_count = 0
    # Run through 100 rounds, assert that shuffle happens
    for _ in range(100):
        player_information = game.start_round(bet_size=10)

        # Shuffle should have happened
        if player_information.game_history == []:
            shuffle_count += 1

    assert shuffle_count > 0


def test_dealer_hand_is_visible_after_round_complete(game):
    # First round
    player_information = game.start_round(bet_size=10)
    player_information, round_complete = game.apply_action(Action.STAND)

    assert len(player_information.game_history) == 0
    assert round_complete

    # Second round
    player_information = game.start_round(bet_size=10)
    assert len(player_information.game_history) == 1


def test_apply_hit(game):
    player_information = game.start_round(bet_size=10)

    # Mock player hand and next card so we can test hitting only once
    # Card value 12
    game.player_hands = [
        Hand([Card(suit=Suit.SPADES, value=2), Card(suit=Suit.SPADES, value=10)], 10)
    ]

    # Hit card value 5, total 17
    game.deck.draw = lambda: Card(suit=Suit.SPADES, value=5)
    player_information, round_complete = game.apply_action(Action.HIT)

    assert len(player_information.current_game.player_hands[0].cards) == 3
    assert len(player_information.current_game.dealer_hand.cards) == 1
    assert player_information.current_game.player_hands[0].best_value == 17

    assert not round_complete

    # Hit card value 5, total 22
    game.deck.draw = lambda: Card(suit=Suit.SPADES, value=5)
    player_information, round_complete = game.apply_action(Action.HIT)

    assert len(player_information.current_game.player_hands[0].cards) == 4
    assert len(player_information.current_game.dealer_hand.cards) == 1
    assert player_information.current_game.player_hands[0].best_value == 22

    assert round_complete
    assert game.current_hand_index == 1
    assert game.get_player_payout() == 0


def test_apply_cant_hit(game):
    game.start_round(bet_size=10)

    game.player_hands = [
        Hand([Card(suit=Suit.SPADES, value=1), Card(suit=Suit.SPADES, value=10)], 10)
    ]

    # Test that we can't hit when we have blackjack
    with pytest.raises(ValueError) as e:
        game.apply_action(Action.HIT)

    assert "Cannot hit" in str(e.value)


def test_apply_stand(game):
    game.start_round(bet_size=10)

    player_information, round_complete = game.apply_action(Action.STAND)

    assert len(player_information.current_game.player_hands[0].cards) == 2
    assert game.current_hand_index == 1
    assert round_complete


def test_apply_double(game):
    bet_size = 10
    game.start_round(bet_size=bet_size)

    # Mock value 12
    game.player_hands = [
        Hand(
            [Card(suit=Suit.SPADES, value=2), Card(suit=Suit.SPADES, value=10)],
            bet_size,
        )
    ]
    # Mock next card value 5
    game.deck.draw = lambda: Card(suit=Suit.SPADES, value=5)

    # Action
    player_information, round_complete = game.apply_action(Action.DOUBLE)

    # Assert 3 cards, double bet, player's hand turn over
    assert len(player_information.current_game.player_hands[0].cards) == 3
    assert player_information.current_game.player_hands[0].bet_amount == 2 * bet_size

    assert game.current_hand_index == 1
    assert round_complete

    # Payout double
    game.dealer_hand.cards = [
        Card(suit=Suit.SPADES, value=2),
        Card(suit=Suit.SPADES, value=5),
    ]
    assert game.get_player_payout() == 4 * bet_size


def test_apply_cant_double(game):
    game.start_round(bet_size=10)

    game.player_hands = [
        Hand(
            [Card(suit=Suit.SPADES, value=1), Card(suit=Suit.SPADES, value=10)],
            10,
        )
    ]

    with pytest.raises(ValueError) as e:
        game.apply_action(Action.DOUBLE)

    assert "Cannot double" in str(e.value)


def test_apply_double_multiple_hands(game):
    bet_size = 10
    game.start_round(bet_size=bet_size)

    game.player_hands = [
        Hand(
            [Card(suit=Suit.SPADES, value=2), Card(suit=Suit.SPADES, value=10)],
            bet_size,
        ),
        Hand(
            [Card(suit=Suit.SPADES, value=2), Card(suit=Suit.SPADES, value=10)],
            bet_size,
        ),
    ]

    # Stand on first hand, double on second hand
    game.deck.draw = lambda: Card(suit=Suit.SPADES, value=5)
    player_information, round_complete = game.apply_action(Action.STAND)
    assert not round_complete
    assert player_information.current_hand_index == 1

    player_information, round_complete = game.apply_action(Action.DOUBLE)
    assert round_complete
    assert player_information.current_hand_index == 2

    assert len(player_information.current_game.player_hands[0].cards) == 2
    assert player_information.current_game.player_hands[0].best_value == 12
    assert len(player_information.current_game.player_hands[1].cards) == 3
    assert player_information.current_game.player_hands[1].best_value == 17

    # First hand loses, second hand wins, payout double
    game.dealer_hand.cards = [
        Card(suit=Suit.SPADES, value=10),
        Card(suit=Suit.SPADES, value=5),
    ]
    assert game.get_player_payout() == 4 * bet_size


def test_apply_cant_split(game):
    game.start_round(bet_size=10)

    game.player_hands = [
        Hand([Card(suit=Suit.SPADES, value=1), Card(suit=Suit.SPADES, value=10)], 10)
    ]

    with pytest.raises(ValueError) as e:
        game.apply_action(Action.SPLIT)

    assert "Cannot split" in str(e.value)


def test_apply_split_multiple_hands(game):
    bet_size = 10
    game.start_round(bet_size=bet_size)

    # Mock 2 hands, 2 cards each, bet 10
    game.player_hands = [
        Hand(
            [Card(suit=Suit.SPADES, value=2), Card(suit=Suit.SPADES, value=2)],
            bet_size,
        ),
        Hand(
            [Card(suit=Suit.SPADES, value=2), Card(suit=Suit.SPADES, value=10)],
            bet_size,
        ),
    ]

    # Split first hand
    player_information, round_complete = game.apply_action(Action.SPLIT)

    # Assert still same turn, index on the first of the split
    assert not round_complete
    assert game.current_hand_index == 0

    # Assert 3 hands, 2 cards each, split performed correctly
    assert len(player_information.current_game.player_hands) == 3
    assert len(player_information.current_game.player_hands[0].cards) == 2
    assert len(player_information.current_game.player_hands[1].cards) == 2

    first_hand = player_information.current_game.player_hands[0]
    second_hand = player_information.current_game.player_hands[1]

    assert first_hand.cards[0].value == 2
    assert second_hand.cards[0].value == 2


@pytest.mark.parametrize(
    "test_case, dealer_cards, hit_expected",
    [
        ("dealer hits on 15", [10, 5], True),
        ("dealer hits on 16", [10, 6], True),
        (
            "dealer hits on soft 17",
            [1, 6],
            True,
        ),
        ("dealer stands on hard 17", [10, 7], False),
        ("dealer stands on soft 18", [1, 7], False),
        ("dealer stands on hard 18", [10, 8], False),
    ],
)
def test_dealer_hit(game, test_case, dealer_cards, hit_expected):
    game.start_round(bet_size=10)
    game.dealer_hand.cards = [
        Card(suit=Suit.SPADES, value=dealer_cards[0]),
        Card(suit=Suit.SPADES, value=dealer_cards[1]),
    ]
    _, round_complete = game.apply_action(Action.STAND)
    assert round_complete

    # Dealer should hit
    game._play_dealer()

    # Assert
    assert len(game.dealer_hand.cards) > (2 if hit_expected else 1), test_case
