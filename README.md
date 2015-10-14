# Fargo

### Introduction

Fargo is a dice game, with scoring as follows:

 - Three of a kind `n` is worth 100*`n`, except three 1's count as 1000 points.
 - Any 5 rolled is worth 50.
 - Any 1 rolled is worth 100.

A player begins her turn by rolling 10 dice. Any dice which score points (i.e. 3 of a kind, 1, or 5) are scored and removed, and the player then decides to either 1) keep her points and end her turn; or 2) roll the remaining dice to score more points. If a roll results in 0 additional points, then the turn is over and 0 points are scored. In the event that all 10 dice are used, the points are kept and a second set of 10 dice is rolled.


### Modules
- `fargo.py` initializes the game, with the `turn()` function

- `strat.py` explores some pure strategies for Fargo, involving minimum number of dice, and a minimum score cutoff.

- `firstfargo.py` is a first attempt at writing the fargo function in Python. It also includes some probabilities

