"""
David Ebert
October 4, 2015
Testing Fargo
"""


import random


# Roll function. loud == True shows results
def roll(n, loud = False):
    ans = []
    for i in range(n):
        ans.append(random.randint(1,6))
    if loud == True:
        print(ans)
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


#Combine roll, summarize, and count into one function
def rollResult(nDice, loud = False):
    return result(summarize(roll(nDice, loud=False)))


# Simulate a turn in Fargo
def turn(oldScore=0):
    dice = 10       # initialize by rolling 10 dice
    score = oldScore
    cont = 1

    while cont != "0":
        r = rollResult(dice)
        score += r[0]
        dice = r[1]

        if r[0]==0:             #No score imporvement => lose and turn over.
            score = oldScore
            dice = 0
            print("You lose! Your score is", score)
            return              #End the function if lose

        if r[1]==0:             #No dice left => win.
            print("You win! Your score is", score)
            print("New turn!", "\n", "\n", "\n")
            turn(score)         #Call the function again if win.
            return

        print("Your score is ", score)
        print("You have", r[1], "dice left.")

        cont = input("Do you want to contiune? Type 0 to stop.  ")
        print()

    print("Your score is",score)
    return

#turn()



