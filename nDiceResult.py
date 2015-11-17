from fargo2 import summarize
from fargo2 import result
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


ans = compileResultDict(roll10)
print(ans)
count = sum(ans.values())
print(count)


def makeProbDict(resultDict):
    """
    Given a resultDict from compileResultDict function:
    Change result:repeats to result:probability by dividing each value by
    the sum of all the values.
    """
    count = sum(ans.values())
    return {x:resultDict[x]/count for x in resultDict.keys()}
    
ans = makeProbDict(ans)
print(ans)

