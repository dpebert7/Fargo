from fargo2 import summarize
from fargo2 import result
from math import factorial
from evolution import indiv


listOfProbDicts = [{(50, 0): 0.16666666666666666,
  (0, 0): 0.6666666666666666, (100, 0): 0.16666666666666666},
 {(0, 0): 0.4444444444444444, (200, 0): 0.027777777777777776,
  (100, 1): 0.2222222222222222, (150, 0): 0.05555555555555555,
  (50, 1): 0.2222222222222222, (100, 0): 0.027777777777777776},
 {(1000, 0): 0.004629629629629629, (300, 0): 0.004629629629629629,
  (200, 1): 0.05555555555555555, (250, 0): 0.013888888888888888,
  (50, 2): 0.2222222222222222, (200, 0): 0.018518518518518517,
  (0, 0): 0.2777777777777778, (500, 0): 0.004629629629629629,
  (400, 0): 0.004629629629629629, (100, 2): 0.2222222222222222,
  (150, 1): 0.1111111111111111, (600, 0): 0.004629629629629629,
  (100, 1): 0.05555555555555555}]

# Use "global" to access variable outside of function!

def findEV(ndice, gene):
    """
    This function initializes the process for finding the expected value
    of a gene, given a starting value of 10 dice. This function relies on
    the functions manager and roll, as well as listOfProbDicts, a list
    containing the possible outcomes and probability (as a dictionary)
    of rolling 1-10 dice.
    """
    sVec = [0,0]
    global sVec
    
    manager(ndice, gene)
    
    print("done with tree.")
    print(sVec)
    valueOfGame = sVec[0]/(1-sVec[1])
    print(valueOfGame)
    return valueOfGame
    

def manager(ndice, gene, prob = 1, soft = 0):
    """
    This function is called by findEV and roll. It decides whether or not
    to continue rolling. If yes, then it calls roll to determine the outcome
    of each possible roll. If no, then it updates the golbal variable sVec.
    """
    while len(gene)<ndice:      # If gene is too short, then at least roll once.
        gene.append(1)
    print(gene)
    if soft >= gene[ndice-1]:   # Stop rolling because gene says so
        global sVec
        sVec = [sVec[0]+soft*prob, sVec[1]]  # Add soft score to score vec
        print("end run")
        print(sVec)
        
    else:
        for key in listOfProbDicts[ndice-1]:  # Keep rolling because gene says so
            roll(ndice = ndice,
                 gene = gene,
                 key = key,
                 prob = prob,
                 soft = soft)               # Investigate ALL possible outcomes!

def roll(ndice, gene, key, prob = 1, soft = 0):
    """
    This function determines the outcome of each roll, updating probability,
    ndice, and soft as appropriate. The function also deals with losing and
    winning scenarios.
    """
    print(key)
    global sVec
    newprob = prob*listOfProbDicts[ndice-1][key]
                            # Update probability based on total likelihood of
                            # ending up in this part of the tree
    newsoft = soft + key[0] # Update soft
    newdice = key[1]        # Update number of dice remaining
    
    if key[0] == 0:        #Lose
        print("lose")

    elif newdice == 0:      # Win <= no dice remain
        sVec = [sVec[0]+(newprob*newsoft), sVec[1]+newprob]
        print("win!")
        print(sVec)
    else:                   # Neither win nor lose; go to manager to
                            # Either roll again or tabulate score
        manager(ndice = newdice,
                gene = gene,
                prob = newprob,
                soft = newsoft)
