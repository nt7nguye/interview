import sys
import importlib
import os
from core import BlackjackSimulator


def list_available_strategies():
    """List all available strategy files in the strategies directory."""
    strategies_dir = os.path.join(os.path.dirname(__file__), "strategies")
    strategies = []

    if os.path.exists(strategies_dir):
        for file in os.listdir(strategies_dir):
            if file.endswith(".py") and not file.startswith("__"):
                strategies.append(file[:-3])  # Remove .py extension

    return strategies


def load_player_strategy(strategy_name):
    """Dynamically load a player strategy class."""
    try:
        # Add the current directory to the Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)

        # Import the module directly
        module = importlib.import_module(f"strategies.{strategy_name}")

        # Find the player class in the module
        for attr_name in dir(module):
            if attr_name.endswith("Strategy") and attr_name != "Strategy":
                player_class = getattr(module, attr_name)
                return player_class()

        print(f"Error: Could not find a Strategy class in {strategy_name}.py")
        sys.exit(1)
    except ImportError as e:
        print(f"Error: Strategy '{strategy_name}' not found or could not be imported.")
        print(f"Import error: {e}")
        sys.exit(1)


def main():
    available_strategies = list_available_strategies()

    if len(sys.argv) < 2:
        print("Usage: python run_simulation.py <strategy_name>")
        print("\nAvailable strategies:")
        for strategy in available_strategies:
            print(f"  - {strategy}")
        sys.exit(1)

    strategy_name = sys.argv[1]

    if strategy_name not in available_strategies:
        print(f"Error: Strategy '{strategy_name}' not found.")
        print("\nAvailable strategies:")
        for strategy in available_strategies:
            print(f"  - {strategy}")
        sys.exit(1)

    print(f"Starting simulation with {strategy_name} strategy...")
    player = load_player_strategy(strategy_name)
    simulator = BlackjackSimulator(player, initial_bankroll=10000.0, bet_size=100.0)
    starting_bankroll = simulator.bankroll

    # Run 100 rounds with verbose output for the first 3 rounds
    for i in range(10000):
        simulator.run_round(verbose=(i < 3))

    print("\nFinal Results:")
    print(f"Total rounds played: {simulator.rounds_played}")
    print(f"Final bankroll: ${simulator.bankroll:.2f}")
    print(f"Total won: ${simulator.bankroll - starting_bankroll:.2f}")
    print(
        f"Average return per round: ${((simulator.bankroll - starting_bankroll) / simulator.rounds_played):.2f}"
    )


if __name__ == "__main__":
    main()
