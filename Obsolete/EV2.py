from probDicts import listOfProbDicts

conStrat = [1,1,1,1]
aggStrat = [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000]

# Use "global" to access variable outside of function!

def findEV(gene = [1, 1, 1, 1, 1, 1, 1, 1], ndice = 10):
    """
    This function initializes the process for finding the expected value
    of a gene, given a starting value of 10 dice. This function relies on
    the functions manager and roll, as well as listOfProbDicts, a list
    containing the possible outcomes and probability (as a dictionary)
    of rolling 1-10 dice.
    """

    global sVec
    sVec = [0,0]
    
    while len(gene)<ndice:  #If gene is too short, then at least roll once
        gene.append(1)
    #print(gene)
    
    manager(gene, ndice, prob = 1, soft = 0)
    
    #print(sVec)
    valueOfGame = sVec[0]/(1-sVec[1])
    #print(valueOfGame)
    return valueOfGame
    
    
def manager(gene, ndice, prob = 1, soft = 0):
    """
    This function is called by findEV and roll. It decides whether or not
    to continue rolling. If yes, then it calls roll to determine the outcome
    of each possible roll. If no, then it updates the golbal variable sVec.
    """
    #print(soft)
    #print(tempGene)

    if soft >= gene[ndice-1]:    # End run because gene says so
        global sVec
        sVec = [sVec[0]+soft*prob, sVec[1]]  # Add soft score to score vec
        #print("end run")
        #print(sVec)
        
    else:
        for key in listOfProbDicts[ndice-1]:  # Keep rolling because gene says so
        
            roll(gene = gene,
                 ndice = ndice,
                 key = key,
                 prob = prob,
                 soft = soft)               # Investigate ALL possible outcomes!

def roll(gene, ndice, key, prob = 1, soft = 0):
    """
    This function determines the outcome of each roll, updating probability,
    ndice, and soft as appropriate. The function also deals with losing and
    winning scenarios.
    """
    #print(key)
    global sVec
    newprob = prob*listOfProbDicts[ndice-1][key]
                            # Update probability based on total likelihood of
                            # ending up in this part of the tree
    newsoft = soft + key[0] # Update soft
    newdice = key[1]        # Update number of dice remaining

    if newdice == 0:        # Win <= no dice remain
        sVec = [sVec[0]+(newprob*newsoft), sVec[1]+newprob]
        #print("win!")
        #print(sVec)
        
    else:                   # Neither win nor lose; go to manager to
                            # Either roll again or tabulate score
        manager(gene = gene,
                ndice = newdice,
                prob = newprob,
                soft = newsoft)