# Fargo

### Introduction

Fargo is a dice game, with scoring as follows:

 - Three of a kind `n` is worth `100n` points, except three 1's count as `1000` points.
 - Any 5 rolled is worth `50` points.
 - Any 1 rolled is worth `100` points.

A player begins her turn by rolling 10 dice. Any dice which score points (i.e. 3 of a kind, 1, or 5) are scored and removed, and the player then decides to either 1) keep her points and end her turn; or 2) roll the remaining dice to score more points. After the second roll, points are scored and the player again chooses to keep her points or continue rolling the remaining dice, etcd... If a roll results in 0 points added to the score, then the turn is over and the turn is worth 0 points. In the event that all 10 dice are used, the points are banked and a second set of 10 dice is rolled, etc. Players take turns until one player reaches a score over 10 000 points, at which point everyone else takes one more turn and the player with the highest score wins.


### Main Scripts

- `nDiceResult.py` calculates the results for rolling N = 1-10 dice, then converts those results to a dictionary for each N . The results from `nDiceResult.py` are stored in `probDicts.py` for repeated use.

- `probDicts.py` stores a list of result dictionaries, one for each N = 1-10 dice rolled. Each dictionary's keys are the distinct scoring results as (points_scored:dice_left), and the dictionary's values are the probability of the key's outcome. This data is created by `nDiceResult.py` and used in `EV.py`.

- `EV.py` finds the expected value of a Fargo turn given a strategy vector.

- `EVEvolution.py` Includes the main evolution functions, which are combined with `EV.py` and `probDicts.py` to perform a genetic algorithm. Some results are included at the end.

- `EVEvolution_step.py` is a copy of `EVEvolution.py` that includes step optimization at the end of each generation. (The strongest strategies converged much more frequently with this step optimization.)

- `trialdata.json` includes the results of 100 trials of 1000 strategy vectors with step optimization. It is imported analyzed near the end of `EVEvolution_step.py`. This trial data was created Fall 2016 over the course of 48 hours on a laptop with ~8 GB memory. The data from `trialdata.json` are stored as 100 separate files in the `trial1data` directory.


#### Old Scripts

- `fargo.py` initializes the game, with the `turn()` function

- `strat.py` explores some pure strategies for Fargo, involving minimum number of dice, and a minimum score cutoff.

- `firstfargo.py` is a first attempt at writing the fargo function in Python. It also includes some probabilities

- `maxminscores.ods` is a spreadsheet containing some basic calculations about maximum and minimum possible scores for N = 1-8 dice remaining, as well as some information about number of distinct scoring outcomes resulting from N = 1-8,10 dice.
