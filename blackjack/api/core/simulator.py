from typing import List
from core import Strategy, BlackjackGame, Action


class BlackjackSimulator:
    """Simulates multiple rounds of blackjack with a given player strategy"""

    def __init__(
        self, player: Strategy, initial_bankroll: float = 1000.0, bet_size: float = 10.0
    ):
        self.player = player
        self.bankroll = initial_bankroll
        self.bet_size = bet_size
        self.game = BlackjackGame()
        self.rounds_played = 0

    def run_round(self, verbose: bool = False) -> List[float]:
        """Run a single round of blackjack"""
        # Can't bet less than 1.0
        bet = max(
            self.player.get_bet_size(self.game.get_player_information(), self.bankroll),
            1.0,
        )
        # Deduct bankroll
        if self.bankroll < bet:
            raise ValueError(
                f"Bankroll is negative. Game over. Lasted {self.rounds_played} rounds"
            )
        else:
            self.bankroll -= bet

        state = self.game.start_round(bet)
        round_complete = False

        if verbose:
            print(f"\n========= Round {self.rounds_played + 1} =========")
            print("=== Start ===")
            print(f"Bet size: ${bet:.2f}. Starting bankroll: ${self.bankroll:.2f}")
            print(f"Dealer shows: {state.current_game.dealer_hand.cards[0]}")
            starting_hand = state.current_game.player_hands[0]
            print(
                f"Player starting hand: {[str(card) for card in starting_hand.cards]} (Value: {starting_hand.best_value})"
            )
            print("=== Actions ===")

        while not round_complete:
            current_hand = state.current_game.player_hands[state.current_hand_index]
            possible_actions = self.game.get_possible_actions()
            if self.bankroll < current_hand.bet_amount:
                possible_actions = [
                    action
                    for action in possible_actions
                    if action != Action.DOUBLE and action != Action.SPLIT
                ]
            action = self.player.get_action(state, possible_actions, self.bankroll)
            if verbose:
                print(f"Player action: {action.value}")

            if action == Action.DOUBLE or action == Action.SPLIT:
                # Deduct bankroll
                self.bankroll -= current_hand.bet_amount
            state, round_complete = self.game.apply_action(action)

            if verbose and not round_complete:
                print(f"Current hand: {str(current_hand)}")

        payout = self.game.get_player_payout()
        self.bankroll += payout
        self.rounds_played += 1

        if verbose:
            print("=== End ===")
            # Show each player hand with its value
            for i, hand in enumerate(self.game.player_hands):
                print(
                    f"Player hand {i + 1}: {[str(card) for card in hand.cards]} (Value: {hand.best_value})"
                )
            print(
                f"Dealer's final hand: {[str(card) for card in self.game.dealer_hand.cards]} (Value: {self.game.dealer_hand.best_value})"
            )
            print(f"Round payout: ${payout:.2f}")
            print(f"Final bankroll: ${self.bankroll:.2f}")

        return payout
