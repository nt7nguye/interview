import copy
from enum import Enum
from typing import List, Tuple
from dataclasses import dataclass
from core.card import Card
from core.hand import Hand
from core.deck import Deck
import random


class Action(Enum):
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"
    SPLIT = "split"


@dataclass
class GameState:
    """Represents the visible state of the game to a player"""

    player_hands: List[List[Card]]
    # If the game is in progress, the dealer's hand is only the first card
    # If the game is over, the dealer's hand is complete
    dealer_hand: List[Card]


class BlackjackGame:
    def __init__(self, num_decks: int = 6):
        self.num_decks = num_decks
        self.deck = Deck(num_decks)

        # Game history of the deck
        self.game_history: List[GameState] = []
        self.current_hand_index: int = 0

    def _shuffle_if_needed(self):
        total_cards = 52 * self.num_decks

        # Randomly choose reshuffle point between 60-80% of deck remaining
        reshuffle_point = total_cards * (0.6 + random.random() * 0.2)

        if len(self.deck.cards) < reshuffle_point:
            # Create fresh shuffled deck
            self.deck = Deck(self.num_decks)
            # Reset game history
            self.game_history = []

    def start_round(self, bet_size: int) -> GameState:
        """Start a new round with the given bet"""
        self._shuffle_if_needed()
        self.player_hands = [Hand([self.deck.draw(), self.deck.draw()], bet_size)]
        self.dealer_hand = Hand([self.deck.draw(), self.deck.draw()], 0)
        self.current_hand_index = 0
        return self._get_game_state()

    def _get_game_state(self) -> GameState:
        """Create a GameState object representing current state"""
        return GameState(
            player_hands=[copy.deepcopy(hand.cards) for hand in self.player_hands],
            dealer_hand=copy.deepcopy(self.dealer_hand.cards),
        )

    def apply_action(self, action: Action) -> Tuple[GameState, bool]:
        """Apply player action and return (new_state, is_round_complete)"""
        current_hand = self.player_hands[self.current_hand_index]

        if action == Action.HIT:
            if not current_hand.can_hit:
                raise ValueError(f"Cannot hit on hand {current_hand}")
            current_hand.cards.append(self.deck.draw())
            if current_hand.is_bust:
                return self._next_hand()

        elif action == Action.STAND:
            return self._next_hand()

        elif action == Action.DOUBLE:
            if not current_hand.can_double:
                raise ValueError(f"Cannot double on hand {current_hand}")
            current_hand.cards.append(self.deck.draw())
            current_hand.bet_amount *= 2
            return self._next_hand()

        elif action == Action.SPLIT:
            if not current_hand.can_split:
                raise ValueError(f"Cannot split on hand {current_hand}")
            new_hand = Hand([current_hand.cards.pop()])
            current_hand.cards.append(self.deck.draw())
            new_hand.cards.append(self.deck.draw())
            self.player_hands.insert(self.current_hand_index + 1, new_hand)

        return self._get_game_state(), False

    def _next_hand(self) -> Tuple[GameState, bool]:
        """Move to next hand or finish round if all hands complete"""
        self.current_hand_index += 1
        is_round_complete = self.current_hand_index >= len(self.player_hands)

        if is_round_complete:
            self._play_dealer()

        return self._get_game_state(), is_round_complete

    def _play_dealer(self):
        """Play out dealer's hand according to rules"""
        while self.dealer_hand.best_value < 17:
            self.dealer_hand.cards.append(self.deck.draw())

        # Dealer must hit if they have a soft 17
        if (
            self.dealer_hand.best_value == 17
            and min(self.dealer_hand.possible_values) < 17
        ):
            self.dealer_hand.cards.append(self.deck.draw())

    def get_payouts(self) -> List[float]:
        """Calculate payout multiplier for each hand"""
        dealer_value = self.dealer_hand.best_value
        dealer_bust = self.dealer_hand.is_bust

        payouts = []
        for hand in self.player_hands:
            if hand.is_bust:
                payouts.append(-1)
            elif dealer_bust:
                payouts.append(1)
            else:
                player_value = hand.best_value
                if player_value > dealer_value:
                    payouts.append(1)
                elif player_value < dealer_value:
                    payouts.append(-1)
                else:
                    payouts.append(0)  # Push
        return payouts
