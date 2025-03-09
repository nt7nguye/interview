from typing import List
from core.game import BlackjackGame
from core.player import RandomPlayer


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
            print(f"Round payouts: {payouts}")
            print(f"Total payout: ${total_payout:.2f}")
            print(f"Current bankroll: ${self.bankroll:.2f}")

        return payouts

    def run_simulation(self, num_rounds: int, verbose: bool = False) -> dict:
        """Run multiple rounds and return statistics"""
        starting_bankroll = self.bankroll

        for _ in range(num_rounds):
            self.run_round(verbose=verbose)

        results = {
            "rounds_played": self.rounds_played,
            "total_won": self.total_won,
            "ending_bankroll": self.bankroll,
            "return_percentage": (
                (self.bankroll - starting_bankroll) / (self.bet_size * num_rounds) * 100
            ),
            "average_return_per_round": self.total_won / num_rounds,
        }

        if verbose:
            print("\nSimulation Results:")
            print(f"Rounds played: {results['rounds_played']}")
            print(f"Total won: ${results['total_won']:.2f}")
            print(f"Final bankroll: ${results['ending_bankroll']:.2f}")
            print(f"Return percentage: {results['return_percentage']:.1f}%")
            print(
                f"Average return per round: ${results['average_return_per_round']:.2f}"
            )

        return results


def main():
    """Example usage of the simulator"""
    player = RandomPlayer()
    simulator = BlackjackSimulator(player)

    # Run 100 rounds with verbose output for the first 3 rounds
    for i in range(100):
        simulator.run_round(verbose=(i < 3))

    print("\nFinal Results:")
    print(f"Total rounds played: {simulator.rounds_played}")
    print(f"Final bankroll: ${simulator.bankroll:.2f}")
    print(f"Total won: ${simulator.total_won:.2f}")
    print(
        f"Average return per round: ${simulator.total_won / simulator.rounds_played:.2f}"
    )


if __name__ == "__main__":
    main()
