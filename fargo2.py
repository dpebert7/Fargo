"""
David Ebert
October 4, 2015
Testing Fargo
"""

from random import randint
import random


def roll(n):
    """
    return a vector containgng the result of rolling n dice.
    """
    return [randint(1,6) for x in xrange(n)]

# Summarize the roll results in a dictionary
# with keys 1-6 and values the roll count
def summarize(rollList):
    """
    Return a dictionary containing a summary of rolling n dice
    """
    sumDict = {}
    return {x:rollList.count(x) for x in range(1,7)}


# 1) Count the value of the roll.
# 2) Determine how many dice are left.
def result(sumDict):
    """
    Given a dictionary from summarize, return the resulting score
    and remaining dice.
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



def rollN(nDice):
    """
    Combine roll, summarize, and result into one function.
    
    """
    return result(summarize(roll(nDice)))




def humanTurn(oldScore=0):
    """
    simulate a turn in Fargo with human inputs.
    """
    dice = 10       # initialize by rolling 10 dice
    score = 0
    cont = 1

    while cont != 0:
        r = rollN(dice)
        score += r['score']
        dice = r['dice']

        if r['score'] == 0:      #No score imporvement => lose and turn over.
            score = oldScore
            print("You lose! Your score is", score)
            return oldScore     #End the function if lose

        if dice == 0:           #No dice left => win.
            print("You win! Your score is", score)
            print("New turn!")
            humanTurn(oldScore + score)         #Call the function again if win.
            return

        print("your turn score is", score)
        print("Your round score is ", oldScore)
        print("You have", dice, "dice left.")

        cont = input("Do you want to contiune? Type 0 to stop.  ")
        print()

    print("Your score is",oldScore + score)
    return (oldScore + score)



def conservativeStrat(dice, score):
    """
    The conservative strategy always returns 0, indicating that the turn
    should stop no matter what.
    """
    return 0
    
def aggressiveStrat(dice, score):
    """
    The aggressive strategy always returns 1, indicating that the turn
    should continue no matter what.
    """
    return 1
    
def stopif2dice(dice, score):
    """
    Return 1 if there are more than 2 dice available.
    Else, retrun 0.
    """
    if dice>2:
        return 1
    return 0


def loudMachineTurn(strategyFunction, oldScore = 0):
    """
    simulate a turn in Fargo using a strategy function.
    The strategy function should return 0 to stop or 1 to continue.
    The function includes print statements
    """
    dice = 10       # initialize by rolling 10 dice
    score = 0
    cont = 1

    while cont != 0:
        r = rollN(dice)
        score += r['score']
        dice = r['dice']

        if r['score'] == 0:      #No score imporvement => lose and turn over.
            score = oldScore
            print("You lose! Your score is", score)
            return oldScore     #End the function if lose

        if dice == 0:           #No dice left => win.
            print("You win! Your score is", score)
            print("New turn!")
            #Call the function again if win.
            machineTurn(strategyFunction, oldScore + score) 
            return

        print("your turn score is", score)
        print("Your round score is ", oldScore)
        print("You have", dice, "dice left.")

        cont = strategyFunction(dice, score)
        print()

    print("Your score is",oldScore + score)
    return (oldScore + score)





def machineTurn(strategyFunction, oldScore = 0):
    """
    simulate a turn in Fargo using a strategy function.
    The strategy function should return 0 to stop or 1 to continue.
    The function includes print statements
    """
    dice = 10       # initialize by rolling 10 dice
    score = 0
    cont = 1

    while cont != 0:
        r = rollN(dice)
        score += r['score']
        dice = r['dice']

        if r['score'] == 0:      #No score imporvement => lose and turn over.
            score = oldScore
            return oldScore     #End the function if lose

        if dice == 0:           #No dice left => win.
            #Call the function again if win.
            machineTurn(strategyFunction, oldScore + score) 

        cont = strategyFunction(dice, score)

    return (oldScore + score)


