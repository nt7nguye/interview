from core import RandomPlayer, BlackjackSimulator


def main():
    print("Starting simulation...")
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
