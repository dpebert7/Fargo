"""
This script enumerates all possible outcomes for 1-8,10 dice. 
Following this, the functions compileResultsDict and makeProbDict
create the listOfProbDicts necessary for the expected value function.
"""


import math # Necessary for factorial funcution



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
#  SKIP ROLL 9 :P  #
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


def summarize(rollList):
    """
    Return a dictionary containing a summary of rolling n dice. This is used 
    in compileResultDict
    """
    return {x:rollList.count(x) for x in range(1,7)}


def result(sumDict):
    """
    Given a dictionary from summarize, return the resulting score
    and remaining dice. This is used in compileResultDict
    """
    s = 0

    #Remove triple 1's
    while sumDict[1]>=3:
        sumDict[1] = sumDict[1]-3
        s +=1000

    #Remove other triples
    for i in sumDict:
        while sumDict[i]>=3:
            sumDict[i] = sumDict[i]-3
            s += 100*i

    #Count 1's as 100
    ones = sumDict[1]
    sumDict[1] = sumDict[1]-ones
    s += 100*ones
    
    #Count 5's as 50
    fives = sumDict[5]
    sumDict[5] = sumDict[5]-fives
    s += 50*fives

    #Count Extra Dice
    diceLeft = sum(sumDict.values())
    
    return{'score':s, 'dice':diceLeft}


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
        repeats = math.factorial(sum(summary.values()))
        for i in summary.values():
            repeats = int(repeats/math.factorial(i))
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
    """
    This combines compileResultDict and resultToProbDict in one function.
    """
    return resultToProbDict(compileResultDict(roll_n_list))



"""
The following listOfProbDicts is stored in probDicts.py for more convenient
access without recompiling this entire script every time.
"""
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








###############################################
###############################################
###############################################

"""
I think that what follows below is an obsolete version of EV.py necessary 
before I understood global variables, but I'm not 100% sure. I've commented 
it out for now.

"""
#
#
#
## Use "global" to access variable outside of function!
#
#
#conStrat = [1,1,1,1]
#aggStrat = [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000]
#
#
#
#
#sVec = [0,0]
#
#
#def findEV(ndice, gene):
#    """
#    This function initializes the process for finding the expected value
#    of a gene, given a starting value of 10 dice. This function relies on
#    the functions manager and roll, as well as listOfProbDicts, a list
#    containing the possible outcomes and probability (as a dictionary)
#    of rolling 1-10 dice.
#    """
#    sVec = [0,0]
#    global sVec
#    
#    manager(ndice, gene)
#    
#    print("done with tree.")
#    print(sVec)
#    valueOfGame = sVec[0]/(1-sVec[1])
#    print(valueOfGame)
#    return valueOfGame
#    
#
#def manager(ndice, gene, prob = 1, soft = 0):
#    """
#    This function is called by findEV and roll. It decides whether or not
#    to continue rolling. If yes, then it calls roll to determine the outcome
#    of each possible roll. If no, then it updates the golbal variable sVec.
#    """
#    while len(gene)<ndice:      # If gene is too short, then at least roll once.
#        gene.append(1)
#    print(gene)
#    if soft >= gene[ndice-1]:   # Stop rolling because gene says so
#        global sVec
#        sVec = [sVec[0]+soft*prob, sVec[1]]  # Add soft score to score vec
#        print("end run")
#        print(sVec)
#        
#    else:
#        for key in listOfProbDicts[ndice-1]:  # Keep rolling because gene says so
#            roll(ndice = ndice,
#                 gene = gene,
#                 key = key,
#                 prob = prob,
#                 soft = soft)               # Investigate ALL possible outcomes!
#
#
#def roll(ndice, gene, key, prob = 1, soft = 0):
#    """
#    This function determines the outcome of each roll, updating probability,
#    ndice, and soft as appropriate. The function also deals with losing and
#    winning scenarios.
#    """
#    print(key)
#    global sVec
#    newprob = prob*listOfProbDicts[ndice-1][key]
#                            # Update probability based on total likelihood of
#                            # ending up in this part of the tree
#    newsoft = soft + key[0] # Update soft
#    newdice = key[1]        # Update number of dice remaining
#    
#    if key[0] == 0:        #Lose
#        print("lose")
#
#    elif newdice == 0:      # Win <= no dice remain
#        sVec = [sVec[0]+(newprob*newsoft), sVec[1]+newprob]
#        print("win!")
#        print(sVec)
#    else:                   # Neither win nor lose; go to manager to
#                            # Either roll again or tabulate score
#        manager(ndice = newdice,
#                gene = gene,
#                prob = newprob,
#                soft = newsoft)