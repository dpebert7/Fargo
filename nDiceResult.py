from fargo2 import summarize
from fargo2 import result
from fargo2 import rollN
from math import factorial


roll1 = [[x+1] for x in range(6)]

#6^1 = 6 rolls
#6 distinct rolls
#3 scoring results


roll2 = [[z,y-1] for z in range(1,7) for y in range(2,8) if y>z]

#6^2 = 36 rolls
#21 distinct rolls
#6 scoring results




roll3 = [[z,y-1,x-2]
             for z in range(1,7)
             for y in range(2,8)
             for x in range(3,9)
             if x>y
             if y>z]

#6^3 = 216 rolls
#56 distinct rolls
#13 scoring results




roll4 = [[z,y-1,x-2, w-3]
             for z in range(1,7)
             for y in range(2,8)
             for x in range(3,9)
             for w in range(4,10)
             if w>x
             if x>y
             if y>z]

#6^4 = 1296 rolls
#126 distinct rolls
#25 scoring results





roll5 = [[z,y-1,x-2, w-3, v-4]
             for z in range(1,7)
             for y in range(2,8)
             for x in range(3,9)
             for w in range(4,10)
             for v in range(5,11)
             if v>w
             if w>x
             if x>y
             if y>z]

#6^5 = 7776 rolls
#252 distinct rolls
#39 scoring results



roll6 = [[z,y-1,x-2, w-3, v-4, u-5]
             for z in range(1,7)
             for y in range(2,8)
             for x in range(3,9)
             for w in range(4,10)
             for v in range(5,11)
             for u in range(6,12)
             if u>v
             if v>w
             if w>x
             if x>y
             if y>z]

#6^6 = 46656 rolls
#462 distinct rolls
#59 scoring results





roll7 = [[z,y-1,x-2, w-3, v-4, u-5, t-6]
             for z in range(1,7)
             for y in range(2,8)
             for x in range(3,9)
             for w in range(4,10)
             for v in range(5,11)
             for u in range(6,12)
             for t in range(7,13)
             if t>u
             if u>v
             if v>w
             if w>x
             if x>y
             if y>z]

#6^7 = 279936 rolls
#792 distinct rolls
#87 scoring results





roll8 = [[z,y-1,x-2, w-3, v-4, u-5, t-6, s-7]
             for z in range(1,7)
             for y in range(2,8)
             for x in range(3,9)
             for w in range(4,10)
             for v in range(5,11)
             for u in range(6,12)
             for t in range(7,13)
             for s in range(8,14)
             if s>t
             if t>u
             if u>v
             if v>w
             if w>x
             if x>y
             if y>z]

#6^8 = 1679616 rolls
#1287 distinct rolls
#117 scoring results



####################
## SKIP ROLL 9 :D ##
####################

roll9 = "HOPE I NEVER END UP HERE!"


roll10 = [[z,y-1,x-2, w-3, v-4, u-5, t-6, s-7, r-8, q-9]
             for z in range(1,7)
             for y in range(2,8)
             for x in range(3,9)
             for w in range(4,10)
             for v in range(5,11)
             for u in range(6,12)
             for t in range(7,13)
             for s in range(8,14)
             for r in range(9,15)
             for q in range(10,16)
             if q>r
             if r>s
             if s>t
             if t>u
             if u>v
             if v>w
             if w>x
             if x>y
             if y>z]

#6^10 = 604661761679616 rolls
#3003 distinct rolls
#194 scoring results



def compileResultDict(roll_n_list):
    """
    Given a complete list of unique ways to roll n dice:
    1) summarize() each roll
    2) Count how many repeats the roll has (mississippi permutations),
          i.e. how many times it should occur out of 6^n trials
    3) Figure out the resulting score of the roll using result()
    4) Add result:repeats to resultDict
    """
    resultDict = {}
    for roll in roll_n_list:
        summary = summarize(roll)
        repeats = factorial(sum(summary.values()))
        for i in summary.values():
            repeats = int(repeats/factorial(i))
        res = result(summary)
        if res["score"] ==0:
            # if there is no score, then don't
            # bother counting remaining dice.
            key = (0,0)
        else:
            key = (res["score"], res["dice"])
        if key in resultDict.keys():
            resultDict[key]+=repeats
        else:
            resultDict[key]=repeats

    return(resultDict)


def resultToProbDict(resultDict):
    """
    Given a resultDict from compileResultDict function:
    Change result:repeats to result:probability by dividing each value by
    the sum of all the values. Also remove the (0,0) key, which is a losing
    result.
    """
    count = sum(resultDict.values())
    return {x:resultDict[x]/count for x in resultDict.keys() if x != (0,0)}


def makeProbDict(roll_n_list):
    return resultToProbDict(compileResultDict(roll_n_list))



listOfProbDicts = [makeProbDict(roll1),
                   makeProbDict(roll2),
                   makeProbDict(roll3),
                   makeProbDict(roll4),
                   makeProbDict(roll5),
                   makeProbDict(roll6),
                   makeProbDict(roll7),
                   makeProbDict(roll8),
                   "Hope I don't end up rolling 9",
                   makeProbDict(roll10)]




# Use "global" to access variable outside of function!


conStrat = [1,1,1,1]
aggStrat = [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000]







def findEV(gene = [1, 1, 1, 1, 1, 1, 1, 1], ndice = 10):
    """
    This function initializes the process for finding the expected value
    of a gene, given a starting value of 10 dice. This function relies on
    the functions manager and roll, as well as listOfProbDicts, a list
    containing the possible outcomes and probability (as a dictionary)
    of rolling 1-10 dice.
    """
    sVec = [0,0]
    global sVec
    
    manager(gene, ndice)
    
    #print("done with tree.")
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
    tempGene = gene
    while len(tempGene) < ndice:
        tempGene.append(1)
    #print(soft)
    #print(tempGene)

    if ((ndice != 10) & (soft >= tempGene[ndice-1])):    # End run because gene says so
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
    newprob = prob*listOfProbDicts[ndice-1][key]
                            # Update probability based on total likelihood of
                            # ending up in this part of the tree
    newsoft = soft + key[0] # Update soft
    newdice = key[1]        # Update number of dice remaining

    if newdice == 0:        # Win <= no dice remain
        global sVec
        sVec = [sVec[0]+(newprob*newsoft), sVec[1]+newprob]
        #print("win!")
        #print(sVec)
    else:                   # Neither win nor lose; go to manager to
                            # Either roll again or tabulate score
        manager(gene = gene,
                ndice = newdice,
                prob = newprob,
                soft = newsoft)



"""
RESULTS FROM THE  10-DICE GAME:

Aggressive strategy: [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000]
 - Likelihood of winning: 0.26657920946402586
 - Expected Value: 437.98989858503955
 - Computes in 9 min

Conservative strategy: [1, 1, 1, 1, 1, 1, 1, 1]
 - Likelihood of winning: 0.010480967078189303
 - Expected Value: 838.1760104620182
 - Computes in ~5 seconds

modest stategy: [1, 1, 1, 1, 1000, 1000, 1000, 1000]
 - Likelihood of winning: 0.017375023046330276
 - Expected Value: 935.719971161939
 - Computes in ~1 minute
"""


def listTurn(stratList = [1,1,1,1,1,1,1,1], ndice = 10):
    turnScore = 0
    global turnScore

    listTurnManager(stratList, ndice)

    return turnScore



def listTurnManager(stratList, ndice):
    """
    simulate a turn in Fargo using a strategy list.
    This function will be used as the main part of the fitness function.
    """
    global turnScore
    dice = ndice
    runScore = 0
    cont = 1

    while cont != 0:
        r = rollN(dice)

        if r['score'] == 0:      #No score imporvement => lose and turn over.
            cont = 0
            runScore = 0     #End the function if lose

        elif r['dice'] == 0:           #No dice left => win.
            #Call the function again if win.
            cont = 0
            runScore += r['score']
            turnScore += runScore
            listTurnManager(stratList, ndice) 
            
        else:
            dice = r['dice']
            runScore += r['score']
            if runScore >= stratList[dice-1]:
                turnScore += runScore
                cont = 0
