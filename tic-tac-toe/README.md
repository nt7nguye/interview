## Tic Tac Toe

This is a simple implementation of Tic Tac Toe in Python. 

You're expected to implement the `HumanStrategy` class. Specifically, you're expected to implement the `get_move` method that returns your next move based on the current board state.

The board is a 3x3 grid, represented as a list of lists `(List[List[Piece]])`. Each piece is either `Piece.X`, `Piece.O`, or `Piece.EMPTY`. 

The `get_move` method should take a board as input and return a tuple of the form `(i, j)` where `i` and `j` are the row and column of the move you want to make.

If you make invalid moves, the computer will automatically win.

Also provided is a `ComputerStrategy` class that you can use to benchmark your strategy. Running a simulation will 10 games between your strategy and the computer's strategy.

### Expectations

- Time complexity and Big O does not matter as long as your program runs in a reasonable amount of time. 
- You can use any libraries and algorithmsyou want.
- You can use Google Search and Stack Overflow.
- You can make 3rd party API calls (including to Claude) if you want.

### Running the simulation

The simulation will run 10 games between your strategy and the computer's strategy. In 9 of the games, the computer will go first and play each possible starting move. In the 10th game, you will go first.

Note that you're always the 'O' player and the computer is always the 'X' player.


```bash
python3 run_simulation.py
```

### Running the program with verbose output

```bash
python3 run_simulation.py -v
```
