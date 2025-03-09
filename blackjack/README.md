### Card counting in blackjack

This is a simple blackjack simulator that evaluates the performance of different blackjack strategies.

You're expected to submit a strategy (in `submitting.py`) that will be evaluated on how much money you make (or lose) over 10000 rounds, starting with a bankroll of $10000.

Your strategy is expected to inherit from the `Strategy` class in `core/strategy.py`. There are two methods you must implement:

1. `def get_bet_size(self, info: PlayerInformation, bankroll: float) -> float:`: 
    - Determine the amount of money to bet before the round starts. 
    - You can use `bankroll` to check how much money you have left before betting
2. `def get_action(self, info: PlayerInformation, possible_actions: List[Action], bankroll: float) -> Action:`: 
    - Determine the next action for a given hand, these include `HIT`, `STAND`, `DOUBLE`, `SPLIT`.
    - You can use `possible_actions` to check what actions are valid
    - You can use `bankroll` to check how much money you have left before deciding to add more (double / split)

For each of these methods, you'll be given a `PlayerInformation` object that contains all current and past information you need to make a decision.

The `PlayerInformation` object contains the following:

- `current_game`: The current game state (e.g. the dealer's visible card and all of your hands and which turn it is)
- `game_history`: The history of the game (e.g. all the previous cards that have been dealt before)


### Given default strategies

- `random`: A random strategy where you take random actions. This strategy will lose all money within 3000-4000 rounds.
- `simple`: A simple strategy where you follow the basic heuristics of the game. This strategy will lose money in the long run but it is a good baseline.

### Where's the edge?

Without card counting, the house always have the advantage and you lose over the long run. 

The edge comes from card counting, specifically counting to optimize for your chance of getting a blackjack, because blackjacks pay 3:2 instead of 1:1. 

A card counter will keep track of all the cards that have been dealt and calculate the ratio of the high cards (10, J, Q, K, A) to the low cards (2, 3, 4, 5, 6).

When the ratio is high, the card counter will bet more because they're more likely to get a blackjack.

When the ratio is low, the card counter will bet less because the house has the advantage.

A card counter will also adjust their actions slightly based on the count, for example, splitting and doubling down more often when the count is high.

### Running the simulator

Install poetry https://python-poetry.org/docs/#system-requirements.

Then initialize the project with `poetry install`.

```
cd blackjack
cd api
poetry install
```

Then run the simulator with `poetry run python3 run_simulation.py <strategy_name>`. For example, 

```bash
poetry run python3 run_simulation.py random
```

### Submitting your strategy
You're welcome to change the `run_simulation.py` file to test your strategy's EV, variance and other metrics. You're also welcome to use any libraries/3rd party code you want.

However, when we evaluate your strategy, we will expect your code in `submitting.py` to work interchangably with the default `run_simulation.py` and the rest of the `core/` code. 



