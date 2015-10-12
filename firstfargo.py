"""
David Ebert
October 4, 2015
Testing Fargo


NOTE:
To play the game, call the function turn().



SOLVED QUESTIONS:
1) 1) What is the probability of using all 10 dice in a round if you never quit?

            25.5$%



2) What is the probability losing your turn while rolling n dice?

            ______
            Empirical probabilities from rolling 1 000 000 dice

            nDice   prob of not losing
            1       0.3330
            2       0.5544
            3       0.7228
            4       0.8425
            5       0.9231
            6       0.9693
            7       0.9910
            8       0.9985
            9       1
            10      1
            ______



3) After rolling 10 dice, what is the probability of having n dice left over?

            ___
            Empirical probabilities from rolling 10 dice 1 000 000 times

            n       prob having n dice left after rolling 10 dice
            0       0.010573
            1       0.049093
            2       0.12642
            3       0.205351
Most Likely 4       0.243013
            5       0.201677
            6       0.113662
            7       0.042674
            8       0.007537
            9       0.0
            10      0.0
            ___



4) What is the optimal number of dice to stop at?

            ___
            Empirical probabilities from rolling 100 000 turns with limit n

            n       Average score using n as minDice
            0       320.4435
            1       322.0465
            2       650.0425
            3       852.368
    BEST -> 4       927.6375
            5       923.641
            6       885.604
            7       850.238
            8       834.0845
            9       829.2515
            10      829.8645

            Note that n=0 and n=1 are the same strategy.
            Likewise, n=9 and n=10 are the stame strategy.
            ___



5) What is the average value of simply rolling 10 dice?

            Average of 1 000 000 iterations is 829.801





6) What is the average value of rolling n dice?

            Empirical probabilities from rolling n dice 100 000 times

            n       Average score using n as minDice
            0       0
            1       25.1125
            2       49.834
            3       86.8835
            4       141.35
            5       215.77
            6       307.7675
            7       419.30
            8       544.0375
            9       682.018
            10      828.8305


UNSOLVED QUESTIONS:

What is the expected value of a turn?
Is there a low points threshold at which it would be worthwhile going for extra points
   even if only one or two dice are left to roll? (e.g. scores less than 400)?
What is the average number of rolls in a turn?






"""


import random


# Roll function with results shown
def loudRoll(n):
    ans = []
    for i in range(n):
        ans.append(random.randint(1,6))
    print(ans)
    return ans


# Roll function with results NOT shown
# Is there a better way of doing this?
def quietRoll(n):
    ans = []
    for i in range(n):
        ans.append(random.randint(1,6))
    return ans


# Summarize the roll results in a dictionary
# with keys 1-6 and values the roll count
def summarize(rollList):
    sumDict = {}
    for i in range(1,7,1):
        sumDict[i]=0
        for j in rollList:
            if i==j:
                sumDict[i]+=1
    return(sumDict)

def rollN(nDice):
    return result(summarize(quietRoll(nDice)))


# 1) Count the value of the roll.
# 2) Determine how many dice are left.
def result(sumDict):
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
    
    return(s, diceLeft)


# Simulate a turn in Fargo
def turn(oldScore=0):
    dice = 10       # initialize by rolling 10 dice
    score = oldScore
    cont = 1

    while cont != "0":
        r = result(summarize(loudRoll(dice)))
        score += r[0]
        dice = r[1]

        if r[0]==0:             #No score imporvement => lose and turn over.
            score = oldScore
            dice = 0
            print("You lose! Your score is", score)
            print()
            return              #End the function if lose

        if r[1]==0:             #No dice left => win.
            print("You win! Your score is", score)
            print("New turn!")
            print()
            turn(score)         #Call the function again if win.
            return

        print("Your score is ", score)
        print("You have", r[1], "dice left.")

        cont = input("Do you want to contiune? Type 0 to stop.  ")
        print()

    print("Your score is",score)
    return

#turn()


# Find the score if there is NO quitting! 
def davidParkerStrategy(oldScore=0):
    r = result(summarize(loudRoll(10)))
    score = oldScore + r[0]
    dice = r[1]
    cont = 1

    while cont != 0:
        r = result(summarize(loudRoll(dice)))
        score += r[0]
        dice = r[1]

        if r[0]==0:
            score = oldScore
            dice = 0
            print("You lose! Your score is", score)
            return(score)

        if r[1]==0:
            print("You win! Your score is", score)
            davidStrategy(score)
            return(score)

#davidParkerStrategy()


"""
1) What is the probability of using all 10 dice in a round if you never quit?   
"""

# Return 1 if all 10 dice are used in a round
# Return 0 if lose
def binaryDavidParkerStrategy():
    r = result(summarize(quietRoll(10)))
    dice = r[1]
    cont = 1

    while cont != 0:
        r = result(summarize(quietRoll(dice)))
        dice = r[1]

        if r[0]==0:
            return(0)

        if r[1]==0:
            return(1)

# Run the above function repeatedly to find the probability
# of using all 10 dice in a round.
def testDavidParkerStrategy(n):
    result = []
    wins = 0
    for i in range(n):
        wins += binaryDavidParkerStrategy()
    return(wins/n)
        

#result = testDavidParkerStrategy(1000)
#print(result)

# Testing this result with n = 1 000 000 returns an average of at least 25.5%!




"""
2) What is the probability losing your turn while rolling n dice?
"""

# Return 0 if rolling n dice makes you end your turn.
def winOrLose(nDice):
    r = result(summarize(quietRoll(nDice)))
    if r[0]==0:
        return 0
    else:
        return 1


# Roll 1-8 dice nRolls times.
# Keep track of non-losing percentage in resultDict
# Note that rolling 9 or 10 dice is ALWAYS safe, so no need to test.

def testRoll(nRolls):
    resultDict = {}
    for i in range(1,9,1):
        resultDict[i]=0
        for j in range(nRolls):
            resultDict[i]+= winOrLose(i)
        resultDict[i]=resultDict[i]/nRolls
    return(resultDict)
            
        

#ans = testRoll(1000)
#print(ans)


"""
Empirical probabilities from rolling 1 000 000 dice

nDice   prob of not losing
1       0.3330
2       0.5544
3       0.7228
4       0.8425
5       0.9231
6       0.9693
7       0.9910
8       0.9985
9       1
10      1
"""






"""
3) After rolling 10 dice, what is the probability of having n dice left over?
"""

def howManyDiceLeft(n):
    return(result(summarize(quietRoll(n)))[1])


def testDiceLeft(nRolls):
    resultDict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
    for i in range(nRolls):
        newResult = howManyDiceLeft(10)
        resultDict[newResult]+=1
    for i in resultDict:
        resultDict[i]=resultDict[i]/nRolls
    return(resultDict)

#ans = testDiceLeft(1000000)
#print(ans)


"""
Empirical probabilities from rolling 10 dice 1 000 000 times

n       prob having n dice left after rolling 10 dice
0       0.010573
1       0.049093
2       0.12642
3       0.205351
4       0.243013
5       0.201677
6       0.113662
7       0.042674
8       0.007537
9       0.0
10      0.0
"""






"""
4) What is the optimal number of dice to stop at?
"""

def turnWithLimit(minDice, oldScore=0):
    dice = 10       # initialize by rolling 10 dice
    score = oldScore

    while dice >= minDice:
        r = result(summarize(quietRoll(dice)))
        score += r[0]
        dice = r[1]

        if r[0]==0:             #No score imporvement => lose and turn over.
            score = oldScore
            dice = 0
            #print("You lose! Your score is", score)
            #print()
            return(score)       #End the function if lose

        if r[1]==0:             #No dice left => win.
            #print("You win! Your score is", score)
            #print("New turn!")
            #print()
            turnWithLimit(minDice=minDice, oldScore = score)         #Call the function again if win.
            return(score)

        #print("Your score is ", score)
        #print("You have", r[1], "dice left.")

        #print()

    #print("Your score is",score)
    return(score)

#turnWithLimit(minDice = 3)

def testLimitExpectation(nRolls):
    resultDict = {}
    for i in range(0,11):
        sumResults = 0
        for j in range(nRolls):
            sumResults += turnWithLimit(i)
        resultDict[i]=sumResults/nRolls
    return(resultDict)


#ans = testLimitExpectation(1000)
#print(ans)



"""
Empirical probabilities from rolling 100 000 turns with limit n

n       Average score using n as minDice
0       320.4435
1       322.0465
2       650.0425
3       852.368
4       927.6375
5       923.641
6       885.604
7       850.238
8       834.0845
9       829.2515
10      829.8645

Note that n=0 and n=1 are the same strategy.
Likewise, n=9 and n=10 are the stame strategy.
"""


"""
What is the average value of simply rolling 10 dice? Average of 1 000 000
iterations is 829.801
"""
def testRollAverage(nRolls):
    total = 0
    for i in range(nRolls):
        total += rollN(10)[0]
    return total/nRolls

#ans = testRollAverage(1000)
#print(ans)

def averageNdice(nRolls):
    resultDict = {}
    for i in range(1,11,1):
        total = 0
        for j in range(nRolls):
            total += rollN(i)[0]
        resultDict[i]=total/nRolls
    return resultDict

#ans = averageNdice(1000)
#print(ans)


"""
What is the average value of simply rolling n dice?

Empirical probabilities from rolling n dice 100 000 times

n       Average score using n as minDice
0       0
1       25.1125
2       49.834
3       86.8835
4       141.35
5       215.77
6       307.7675
7       419.30
8       544.0375
9       682.018
10      828.8305

Note that n=0 and n=1 are the same strategy.
Likewise, n=9 and n=10 are the stame strategy.
"""

