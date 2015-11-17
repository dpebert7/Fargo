import fargo


# Return 1 if house is run, otherwise 0.
def allOrNothing():
    dice = 10       # initialize by rolling 10 dice
    cont = 1

    while cont !=0:
        r = fargo.rollResult(dice)
        dice = r[1]

        if r[0]==0:             #No score imporvement => lose and turn over.
            return 0            #End the function if lose

        if r[1]==0:             #No dice left => win, end function
            return 1

def testAllOrNothing(nTrials):
    nWins=0
    for i in range(nTrials):
        nWins+=allOrNothing()
    return nWins/nTrials

ans = testAllOrNothing(100)
print(ans)
