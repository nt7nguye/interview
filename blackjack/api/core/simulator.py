from typing import List
from .game import BlackjackGame


class BlackjackSimulator:
    """Simulates multiple rounds of blackjack with a given player strategy"""

    def __init__(
        self, player, initial_bankroll: float = 1000.0, bet_size: float = 10.0
    ):
        self.player = player
        self.bankroll = initial_bankroll
        self.bet_size = bet_size
        self.game = BlackjackGame()
        self.rounds_played = 0
        self.total_won = 0.0

    def run_round(self, verbose: bool = False) -> List[float]:
        """Run a single round of blackjack"""
        state = self.game.start_round(self.bet_size)
        round_complete = False

        if verbose:
            print(f"\nRound {self.rounds_played + 1}")
            print(f"Dealer shows: {state.dealer_up_card}")
            print(f"Player hands: {[str(card) for card in state.player_hands[0]]}")

        while not round_complete:
            action = self.player.get_action(state)
            if verbose:
                print(f"Player action: {action.value}")

            state, round_complete = self.game.apply_action(action)

            if verbose and not round_complete:
                current_hand = state.player_hands[state.current_hand_index]
                print(f"Current hand: {[str(card) for card in current_hand]}")

        payouts = self.game.get_payouts()
        total_payout = sum(payout * self.bet_size for payout in payouts)
        self.bankroll += total_payout
        self.total_won += total_payout
        self.rounds_played += 1

        if verbose:
            # Show each player hand with its value
            for i, hand in enumerate(self.game.player_hands):
                print(
                    f"Player hand {i + 1}: {[str(card) for card in hand.cards]} (Value: {hand.best_value})"
                )
            print(
                f"Dealer's final hand: {[str(card) for card in self.game.dealer_hand.cards]} (Value: {self.game.dealer_hand.best_value})"
            )
            print(f"Round payouts: {payouts}")
            print(f"Total payout: ${total_payout:.2f}")
            print(f"Current bankroll: ${self.bankroll:.2f}")

        return payouts
