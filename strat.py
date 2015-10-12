import fargo

#Create expected value dictionary for rolling 1-10 nDice
def createExpValDict(nRolls):
    resultDict = {}
    for i in range(1,11,1):
        total = 0
        for j in range(nRolls):
            score = fargo.rollResult(i)[0]
            total += score
        resultDict[i]=total/nRolls
    return resultDict

#ans = createExpValDict(100000)
#print(ans)
expVal = {1: 24.8585, 2: 49.6105, 3: 87.284, 4: 141.2715, 5: 214.8215, 6: 309.2175, 7: 421.3585, 8: 545.1145, 9: 684.0025, 10: 828.038}

#Create p_continuing value dictionary for rolling 1-10 nDice
def createp_contDict(nRolls):
    resultDict = {9:1, 10:1}
    for i in range(1,9,1):
        nCont = 0
        for j in range(nRolls):
            score = fargo.rollResult(i)[0]
            if score > 1:
                nCont+=1
        resultDict[i]=nCont/nRolls
    return resultDict


#p_cont = createp_contDict(100000)
#print(p_cont)

#p_cont initialized from 100 000 trials
p_cont = {1: 0.33493, 2: 0.5556, 3: 0.7211, 4: 0.84397, 5: 0.92198, 6: 0.96826, 7: 0.99096, 8: 0.99844, 9: 1, 10: 1}

def multDict(a,b):
    return {x:a[x]*b[x] for x in a.keys()}
conserveDict = multDict(expVal, p_cont)



# Create list of parameters
def expandGrid(x,y):
    result = []
    for i in x:
        for j in y:
            result.append([i,j])
    return result





# Need simplified Fargo function that accepts minDice and minScore arguments.
# testAutoTurn is a debugged version of turn() which continues until there are
# only 1 or 2 dice left, unless the score is still below 1000.

def testAutoTurn():
    oldScore = 0
    newTurn = True

    while newTurn == True:
        dice = 10     # initialize by rolling 10 dice, resetting score to 0
        score = 0
        rollOn = True

        while rollOn == True:
            r = fargo.rollResult(dice)
            score += r[0]
            dice = r[1]

            if r[0]==0:             #No score imporvement => lose and turn over.
                score = 0
                print("You lose! Your score is", oldScore)
                rollOn = False
                newTurn = False
                return oldScore     #End the function if lose

            if r[1]==0:             #No dice left => win.
                print("You win! Your score is", score, "... New turn!!!", "\n")
                oldScore += score
                rollOn = False
                newTurn = True      #Call the function again if win.

            if dice !=0:
                print("Your score is ", score,"... You have", r[1], "dice left.")
                if dice<=2 and score>=1000:
                    rollOn = False
                    newTurn = False
                    print("Your score is", score)
                    return(score + oldScore)

"""
for i in range(10):
    print("\n", "GAME", i)
    ans = testAutoTurn()
    print(ans)
"""




# Rewrite autoTurn to accept a min-dice Argument
# and a scoreOverrule threshold

# e.g. diceVeto = 3 and scoreOverrule = 700 means
# stop if there are 3 or fewer dice, unless the score is below 700
"""
def testAutoTurn(diceVeto, scoreOverrule):
    #print("New Turn", "diceVeto:", diceVeto, "scoreOverrule:", scoreOverrule)
    oldScore = 0
    newTurn = True

    while newTurn == True:
        dice = 10     # initialize by rolling 10 dice, resetting score to 0
        score = 0
        rollOn = True

        while rollOn == True:
            r = fargo.rollResult(dice)
            score += r[0]
            dice = r[1]

            if r[0]==0:             #No score imporvement => lose and turn over.
                score = 0
                #print("You lose! Your score is", oldScore)
                rollOn = False
                newTurn = False
                return oldScore     #End the function if lose

            if r[1]==0:             #No dice left => win.
                #print("You win! Your score is", score, "... New turn!!!", "\n")
                oldScore += score
                rollOn = False
                newTurn = True      #Call the function again if win.

            if dice !=0:
                #print("Your score is ", score,"... You have", r[1], "dice left.")
                if dice<=diceVeto and score>=scoreOverrule:
                    rollOn = False
                    newTurn = False
                    #print("Your score is", score)
                    return(score + oldScore)
"""

# More efficient, with prints removed.
def testAutoTurn(diceVeto, scoreOverrule):
    oldScore = 0
    newTurn = True

    while newTurn == True:
        dice = 10     # initialize by rolling 10 dice, resetting score to 0
        score = 0
        rollOn = True

        while rollOn == True:
            r = fargo.rollResult(dice)
            score += r[0]
            dice = r[1]

            if r[0]==0:
                score = 0
                return oldScore

            if r[1]==0:
                oldScore += score
                rollOn = False
                newTurn = True

            if dice !=0:
                if dice<=diceVeto and score>=scoreOverrule:
                    rollOn = False
                    newTurn = False
                    return(score + oldScore)


# Use wide range of expandGrid to set up test iterations.
diceVetoThresholds = [2, 3, 4, 5, 6]
scoreOverruleThresholds = [300, 400, 500, 600, 700, 800, 900]

parameters = expandGrid(diceVetoThresholds, scoreOverruleThresholds)

def testParam(iterations, paramList):
    resultList = []
    for i in range(len(paramList)):
        total = 0
        for j in range(iterations):
            total += testAutoTurn(diceVeto = paramList[i][0], scoreOverrule = paramList[i][1])
        resultList.append(total/iterations)
    return resultList

#ans = testParam(iterations = 1000, paramList = parameters)
#print(ans)
#print(max(ans))

# Z with 100000 iterations
Z = [902.7185, 908.363, 907.9605, 904.645, 889.412, 868.868, 843.089, 959.448, 958.856, 960.8525, 957.848, 943.31, 924.1455, 889.865, 939.229, 940.0825, 947.429, 948.1145, 941.2335, 922.4015, 894.3845, 895.569, 904.4175, 919.672, 928.429, 923.5745, 914.2865, 887.565, 863.943, 882.2845, 901.901, 909.6535, 912.8195, 903.446, 882.307]
X = []
Y = []
for i in parameters:
    X.append(i[0])
    Y.append(i[1])

"""
TRY TO PLOT ON 3D GRAPH:

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111,  projection = '3d')
"""

