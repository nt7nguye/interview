from enum import Enum
from typing import List, Optional, Tuple
from dataclasses import dataclass
from .card import Card
from .hand import Hand
from .deck import Deck


class Action(Enum):
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"
    SPLIT = "split"


@dataclass
class GameState:
    """Represents the visible state of the game to a player"""

    player_hands: List[List[Card]]  # Multiple hands in case of splits
    dealer_up_card: Optional[Card]
    current_hand_index: int
    can_split: bool
    can_double: bool


class BlackjackGame:
    def __init__(self, num_decks: int = 6):
        self.num_decks = num_decks  # Store number of decks for reshuffling
        self.deck = Deck(num_decks)
        self.player_hands: List[Hand] = []
        self.dealer_hand: Hand = Hand([])
        self.current_hand_index: int = 0
        self.bet_amount: int = 0

    def _ensure_cards_available(self, num_cards_needed: int = 1):
        """Ensure there are enough cards available, reshuffle if needed"""
        if len(self.deck.cards) < num_cards_needed:
            print(f"Reshuffling deck. Cards remaining: {len(self.deck.cards)}")
            self.deck = Deck(self.num_decks)  # Create fresh shuffled deck

    def start_round(self, bet: int) -> GameState:
        """Start a new round with the given bet"""
        # Need 4 cards to start a round (2 for player, 2 for dealer)
        self._ensure_cards_available(4)

        self.bet_amount = bet
        self.player_hands = [Hand([self.deck.draw(), self.deck.draw()])]
        self.dealer_hand = Hand([self.deck.draw(), self.deck.draw()])
        self.current_hand_index = 0
        return self._get_game_state()

    def _get_game_state(self) -> GameState:
        """Create a GameState object representing current state"""
        # Check if we've completed all hands
        if self.current_hand_index >= len(self.player_hands):
            return GameState(
                player_hands=[hand.cards for hand in self.player_hands],
                dealer_up_card=self.dealer_hand.cards[0],
                current_hand_index=len(self.player_hands) - 1,  # Return last hand index
                can_split=False,
                can_double=False,
            )

        current_hand = self.player_hands[self.current_hand_index]
        can_split = (
            len(current_hand.cards) == 2
            and current_hand.cards[0].blackjack_value
            == current_hand.cards[1].blackjack_value
            and len(self.player_hands) < 4  # Limit splits to 3 times
        )
        can_double = len(current_hand.cards) == 2

        return GameState(
            player_hands=[hand.cards for hand in self.player_hands],
            dealer_up_card=self.dealer_hand.cards[0],
            current_hand_index=self.current_hand_index,
            can_split=can_split,
            can_double=can_double,
        )

    def apply_action(self, action: Action) -> Tuple[GameState, bool]:
        """Apply player action and return (new_state, is_round_complete)"""
        self._ensure_cards_available()  # Ensure at least one card is available
        current_hand = self.player_hands[self.current_hand_index]

        if action == Action.HIT:
            current_hand.cards.append(self.deck.draw())
            if current_hand.is_bust:
                return self._next_hand()

        elif action == Action.STAND:
            current_hand.stood = True
            return self._next_hand()

        elif action == Action.DOUBLE:
            if len(current_hand.cards) != 2:
                raise ValueError("Can only double on first two cards")
            current_hand.cards.append(self.deck.draw())
            current_hand.doubled = True
            return self._next_hand()

        elif action == Action.SPLIT:
            # Need 2 cards for split (1 for each hand)
            self._ensure_cards_available(2)
            if not self._get_game_state().can_split:
                raise ValueError("Split not allowed")
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
            self._ensure_cards_available()  # Add this check
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

            if hand.doubled:
                payouts[-1] *= 2

        return payouts
