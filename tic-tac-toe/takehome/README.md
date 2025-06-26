Write a program that plays every possible tic-tac-toe game, and then prints the number of possible valid, completed game states.

+ Valid meaning the game can be reached by following the rules of tic-tac-toe.

+ Completed meaning the game is won by either player or tied.

Note:

+ Assume X always goes first

+ If two games end in the same state, they should only be counted once. Below is an example of one valid game state after O move

```
X O X      X O X

X _ _  ->  X O _

_ O _      _ O _


X O X      X O X

X O _  ->  X O _

_ _ _      _ O _
```

+ Est: ~40 mins for completion