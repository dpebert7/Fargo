# Fargo

### Introduction

Fargo is a dice game, with scoring as follows:

 - Three of a kind `n` is worth `100n` points, except three 1's count as `1000` points.
 - Any 5 rolled is worth `50` points.
 - Any 1 rolled is worth `100` points.

A player begins her turn by rolling 10 dice. Any dice which score points (i.e. 3 of a kind, 1, or 5) are scored and removed, and the player then decides to either 1) keep her points and end her turn; or 2) roll the remaining dice to score more points. After the second roll, points are scored and the player again chooses to keep her points or continue rolling the remaining dice, etcd... If a roll results in 0 points added to the score, then the turn is over and the turn is worth 0 points. In the event that all 10 dice are used, the points are banked and a second set of 10 dice is rolled, etc. Players take turns until one player reaches a score over 10 000 points, at which point everyone else takes one more turn and the player with the highest score wins.


### Modules
- `fargo.py` initializes the game, with the `turn()` function

- `strat.py` explores some pure strategies for Fargo, involving minimum number of dice, and a minimum score cutoff.

- `firstfargo.py` is a first attempt at writing the fargo function in Python. It also includes some probabilities

