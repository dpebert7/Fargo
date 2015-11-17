from fargo2 import summarize
from fargo2 import result


roll1 = [[a+1] for a in range(6)]

roll2 = [[a+1, b+1] for a in range(6)
         for b in range(6)]

roll10 = [[a+1, b+1, c+1, d+1, e+1, f+1, g+1]
         for a in range(6)
         for b in range(6)
         for c in range(6)]

roll10 = [[a+1, b+1, c+1, d+1, e+1, f+1, g+1, h+1, i+1, j+1]
         for a in range(6)
         for b in range(6)
         for c in range(6)
         for d in range(6)
         for e in range(6)
         for f in range(6)
         for g in range(6)
         for h in range(6)
         for i in range(6)
         for j in range(6)]

roll10 = [[a+1, b+1, c+1, d+1, e+1, f+1, g+1, h+1, i+1, j+1]
         for a in range(6)
         for b in range(6)
         for c in range(6)
         for d in range(6)
         for e in range(6)
         for f in range(6)
         for g in range(6)
         for h in range(6)
         for i in range(6)
         for j in range(6)]




def compileResultDict(roll_n_list):
    resultDict = {}
    for roll in roll_n_list:
        res = result(summarize(roll))
        if res["score"] ==0:
            key = (0,0)
        else:
            key = (res["score"], res["dice"])
        if key in resultDict.keys():
            resultDict[key]+=1
        else:
            resultDict[key]=1

    return(resultDict)




