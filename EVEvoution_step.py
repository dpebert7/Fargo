"""
This is a modification of the EVEvolution.py script that includes step 
optimization for each vector in the population
"""

#import os
#os.getcwd()
#os.chdir("/home/david/Desktop/Documents/GitRepos/Fargo")

from EV import findEV
from operator import add
from random import randint
from random import random
import functools

import matplotlib.pyplot as plt # for plots
import pylab

import json # for data


def myround(x, base = 50):
    """
    round a nunmber to the nearest 50. This function is (sometimes) used 
    in the evolve function to round children to the nearest 50.
    """
    return int(base*round(float(x)/base))


def indiv():
    """
    create a member of the Fargo strategy vector population. Each individual
    should have a reasonabble max and min threshold
    """
    vector = []
    vector.append(randint(9, 61)*50) #from 450 to 3050
    vector.append(randint(8, 45)*50) #from 400 to 2250
    vector.append(randint(7, 43)*50) #from 350 to 2150
    vector.append(randint(6, 41)*50) #from 300 to 2050
    vector.append(randint(5, 25)*50) #from 250 to 1250
    vector.append(randint(4, 23)*50) #from 200 to 1150
    vector.append(randint(3, 21)*50) #from 150 to 1050
    vector.append(randint(2, 5)*50)  #from 100 to 250
    return vector


def pop(count):
    """
    Create a number of strategy vectors (i.e. a population).
    count: the number of strategies in the population
    """
    return [ indiv() for x in range(count) ]


conservativeList = [50 for i in range(8)]
aggressiveList = [5000 for i in range(8)]
    
        
def fitFun(individual):
    """
    Use the expected value function from nDiceResult.py to find the
    "fitness" (i.e. EV) of a strategy vector.
    This replaces the iterative fitness function from iterateEvolution.py.
    """
    return findEV(ndice = 10, gene = individual)

# fitFun(conservativeList, 10)
# fitFun(aggressiveList, 10)



def gradePop(pop):
    """
    Find average fitness for a population of strategy vectors.
    """    
    summed = functools.reduce(add, (fitFun(x) for x in pop), 0)
    return summed / (len(pop) * 1.0)

#gradePop([conservativeList, aggressiveList],10)
#gradePop(pop(10), 10)


def findStrongest(pop):
    """
    Return the "strongest" strategy vector from a population.
    """
    graded = [ (fitFun(x), x) for x in pop ]
    graded = [ x[1] for x in sorted(graded) ]
    graded.reverse()
    return graded[0]

def evolve(pop, retain=0.25, add_random=0.01, mutate=0.02, elite = 0):
    """
    Evolve function for Fargo.
    pop: starting population list
    retain: fraction of population which will parent the next generation
    add_random: fraction of population to be created randomly
    mutate: fraction of population that will  mutate
    elite: fraction of population from the top that will
    automatically move on to next generation without mutation
    """
    # Linearly Optimize
    pop = [stepOptimize(x)["thebest"] for x in pop]

    # Sort strongest to weakest
    graded = [ (fitFun(x), x) for x in pop ]
    graded = [ x[1] for x in sorted(graded) ]
    graded.reverse()

    # Determine and save the "elites"
    elites = elites_length = int(len(graded)*elite)
    elites = graded[:elites_length]
    
    # Determine parents of next generation
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]

    # Add a few other random individuals to promote genetic diversity
    add_length = int(len(graded)*add_random)
    for i in range(add_length):
        parents.append(indiv())


    # Randomly mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, 7)
            tempMutant = indiv()
            individual[pos_to_mutate] = tempMutant[pos_to_mutate]

    
    # crossover parents to create children using splicing
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            switchLocation = randint(1,len(male)-1)
            child = male[:switchLocation] + female[switchLocation:]
            children.append(child)
    
    """
    # crossover parents to create children using rounded average
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            child = [ myround((male[x]+female[x])/2) for x in range(len(male)) ]
            children.append(child)
    """
    
    parents.extend(children)
    parents[:elites_length] = elites
    
    return parents


###################################
## IMPORTANT STARTING PARAMATERS ##
###################################

#populationSize = 1000
#generations = 25

#retain = 0.25
#add_random = 0.02
#mutate = 0.01
#elite = 0.0
###################################

def EVevolution(index, populationSize, generations, retain, add_random, mutate, elite):
    """
    Perform genetic algorithm. 
    Data are also stored to .json using savedata and plotted using makeplot.
    """
    #Make starting population
    p = pop(populationSize)

    #Store fitness history
    population_history = [p]

    average_fitness_history = [gradePop(p)]

    strongest = findStrongest(p)
    strongest_history = [strongest]
    strongest_fitness_history = [fitFun(strongest)]

    #Run evolution
    for i in range(generations):
        p = evolve(pop = p,
                   retain = retain,
                   add_random = add_random,
                   mutate = mutate,
                   elite = elite)
                   
        population_history.append(p)
            
        new_population_average_fitness = gradePop(p)
        average_fitness_history.append(new_population_average_fitness)
        
        new_population_strongest = findStrongest(p)
        strongest_history.append(new_population_strongest)
        strongest_fitness = fitFun(new_population_strongest)
        strongest_fitness_history.append(strongest_fitness)
        
        print ("trial " + str(index), "generation "+ str((i+1)), 
               new_population_average_fitness, strongest_fitness)
    
    print(strongest_history)
    print(strongest_fitness_history)
    
    makeplot(strongest_fitness_history, average_fitness_history)
    savedata("trial"+str(index)+".json", 
             strongest_history, average_fitness_history, 
             strongest_fitness_history, 
             populationSize, 
             generations, 
             elite, 
             mutate, 
             add_random)
    return

def makeplot(strongest_fitness_history, average_fitness_history):
    """
    Given a list of strongest_fitness_history and average_fitness_history,
    plot both on a line graph.
    """
    plt.plot(strongest_fitness_history, "b-", label = "EV of Best Strategy")
    plt.plot(average_fitness_history, "r--", label = "EV of Average Strategy")
    pylab.ylim([675,975])
    plt.xlabel("Generations")
    plt.ylabel("Expected Value")
    plt.legend(loc = 4)
    plt.show()


def savedata(unique_file_name, 
             strongest_history, 
             average_fitness_history, 
             strongest_fitness_history, 
             populationSize, 
             generations, 
             elite, 
             mutate, 
             add_random):
    """
    Save trial data to a .json file called "unique_file_name"
    """
    f = open(unique_file_name, "w")
    json.dump({"strongest_history":strongest_history,
               "average_fitness_history":average_fitness_history, 
               "strongest_fitness_history":strongest_fitness_history,
               "populationSize":populationSize,
               "generations":generations,
               "elite":elite,
               "mutate":mutate,
               "add_random":add_random}, 
               f)
    f.close()


def evolutionRevolution(ntrials, 
                        populationSize = 1000, 
                        generations = 25, 
                        retain = 0.25, 
                        add_random = 0.2, 
                        mutate = 0.01, 
                        elite = 0.0):
    """
    Repeat EVevolution ntrials times. Note that data from all trials 
    are stored in a .json file.
    """
    for i in range(ntrials):
        EVevolution(index = (i+1), 
                    populationSize = populationSize, 
                    generations = generations, 
                    retain = retain, 
                    add_random = add_random, 
                    mutate = mutate, 
                    elite = elite)
        print("Done with trial " + str(i+1))
    print("Done with everything! Hooray!")
    return

#evolutionRevolution(100)
# this is 100 trials of 25 generations of 1000 strategies. 
# If one generation takes about 70 seconds to run then this should compile in about 2 days.

"""
#read values back into Python and store as one big .json file 
biglist = []
for i in range(100):
    f = open("trial" + str(i+1) + ".json")
    temp = json.load(f)
    f.close()
    biglist.append(temp)


f = open("trialdata.json", "w")
json.dump(biglist, f)
f.close()
"""


# To load data, use the following:
"""
f = open("unique_file_name.txt", "r")
x = json.load(f)
f.close()
"""

"""
HISTORY:

# 500 starting population
# 25 generations
# Trial 1 strongest: 962.333623 (Converged after 13 generations)
# [500, 400, 550, 1150, 1250, 1150, 1050, 250, 1, 1]
# Trial 2 strongest: 962.25544795318 (Converged after 18 gens)
# [500, 400, 550, 1000, 1250, 1150, 1050, 250, 1, 1]
# Trial 3 strongest: 962.3112546635437 (Converged after 11 gens)
# [550, 400, 550, 1100, 1250, 1150, 1050, 250, 1, 1]


# 1000 population (takes about 30 minutes to run 25 generations)
# 25 generations
# Trial 1 strongest: 962.285183184285 (Converged after 17)
# [550, 450, 500, 1150, 1250, 1150, 1050, 250, 1, 1]
# Trial 2 strongest: 961.8071403552686 (Converged after 9)
# [550, 400, 500, 1150, 1200, 1150, 1050, 250, 1, 1]

# 5000 population
# 25 generations
# Trial 1 strongest: 962.3343332342337
# [550, 400, 550, 1150, 1250, 1150, 1050, 250, 1, 1]

# 10000 population
# 25 generations
# Trial 1 strongest: 962.3343332342337
# [550, 400, 550, 1150, 1250, 1150, 1050, 250, 1, 1]
"""

f = open("trialdata.json", "r")
trialdata = json.load(f)
f.close()


"""
# make a big plot for the data
plt.plot(trialdata[0]["strongest_fitness_history"], "b-", label = "EV of Best Strategy")
plt.plot(trialdata[0]["average_fitness_history"], "r-", label = "Average EV of Population")
for i in range(len(trialdata)-1): 
    plt.plot(trialdata[i+1]["strongest_fitness_history"], "b-")
    plt.plot(trialdata[i+1]["average_fitness_history"], "r-")
pylab.ylim([740,970])
plt.xlabel("Generations")
plt.ylabel("Expected Value")
plt.legend(loc = 4)
"""


"""
#plot showing strongest_fitness_history
plt.plot(trialdata[0]["strongest_fitness_history"], "b-", label = "EV of Best Strategy")
for i in range(len(trialdata)-1): 
    plt.plot(trialdata[i+1]["strongest_fitness_history"], "b-")
pylab.ylim([960,963])
plt.xlabel("Generations")
plt.ylabel("Expected Value of Best Strategy")
plt.legend(loc = 1)
"""

thebest = [550, 400, 550, 1150, 1250, 1150, 1050, 250, 1, 1]
decent = [550, 400, 600, 1100, 1250, 1150, 1050, 250, 1, 1]
worstest = [1000, 400, 200, 700, 400, 1150, 1050, 150, 1, 1]


#%%
def stepOptimize(strategy_vector):
    """
    This function takes a strategy vector and repeatedly searches for local optima
    by repeatedly incrementing each entry up and down by 50.
    """
    #Initialize lists of EV and stretegy vectors    
    EVlist = [findEV(strategy_vector)]
    strategyVectorList = [strategy_vector]
    keepGoing = True
    count = 1
    
    while keepGoing == True:
        #Set up copy
        copy = [i for i in strategyVectorList[-1]]
        newStrategy = [i for i in strategyVectorList[-1]]
        newEV = findEV(copy)
        
        #Increment the values of copy up and down by 50
        for index in range(8):
            copy[index]+=50
            if findEV(copy)>newEV:
                newStrategy = [i for i in copy]
                newEV = findEV(newStrategy)
            copy[index]-=100
            if findEV(copy)>newEV:
                newStrategy = [i for i in copy]
                newEV = findEV(newStrategy)
            copy[index]+=50
            
        # Record new values OR end while loop
        if(newEV > EVlist[-1]):
            EVlist.append(findEV(newStrategy))        
            strategyVectorList.append(newStrategy)
            keepGoing = True
        else:
            keepGoing = False
        
        if(count<100):
            count+=1
        else:
            print("This is the end of the line")
            keepGoing = False

    return {"strategyVectorList":strategyVectorList, 
            "EVlist":EVlist,
            "thebest":strategyVectorList[-1],
            "maxEV":EVlist[-1]}

#%%


endingStrongest = [trialdata[i]["strongest_history"][-1] for i in range(100)]
endingEVs = [trialdata[i]["strongest_fitness_history"][-1] for i in range(100)]
#optimizedStrongest = [stepOptimize(endingStrongest[i])["strategy_vector"] for i in range(100)]
#sum([i == thebest for i in optimizedStrongest]) 
#in 54 cases, the strategy can be linearly optimized to reach thebest
endingEVs = [trialdata[i]["strongest_fitness_history"][-1] for i in range(100)]
sum([i==962.3343332342337 for i in endingEVs])
#in 8 cases, the hightest EV was ALREADY the same as that of thebest


def aggressiveness(strategy_vector):
    """
    This function returns a vector where each entry gives the fraction 
    of plausible strategies that are less aggressive at that entry.
    """
    vector = []
    vector.append(float((strategy_vector[0]-450)/float(50*52))) 
        #450 to 3050, 52 vals
    vector.append(float((strategy_vector[1]-400)/float(50*37))) 
        #400 to 2250, 37 vals
    vector.append(float((strategy_vector[2]-350)/float(50*36))) 
        #350 to 2150, 36 vals
    vector.append(float((strategy_vector[3]-300)/float(50*35))) 
        #300 to 2050, 35 vals
    vector.append(float((strategy_vector[4]-250)/float(50*20))) 
        #250 to 1250, 20 vals
    vector.append(float((strategy_vector[5]-200)/float(50*19))) 
        #200 to 1150, 19 vals
    vector.append(float((strategy_vector[6]-150)/float(50*18))) 
        #150 to 1050, 18 vals
    vector.append(float((strategy_vector[7]-100)/float(50*3)))  
        #100 to 250, 4 vals
    return vector

"""
#bar plot showing the values of a strategy
bar_width = 1
plt.bar([i+1 for i in range(8)],thebest[0:8],
         bar_width,
         color = "b",
         align = "center")
plt.title("When to Stop Rolling")
plt.xlabel("Number of Dice Remaining")
plt.ylabel("Number of Points at which to Stop Rolling")
plt.xticks(np.arange(8)+1, ("1", "2", "3", "4", "5", "6", "7", "8"))
plt.tight_layout()
plt.show()
"""

"""
#bar plot showing the aggressiveness of a strategy
bar_width = 1
plt.bar([i+1 for i in range(8)],aggressiveness(thebest), 
         bar_width,
         color = "b",
         align = "center")
plt.title("Aggressiveness of Best Strategy")
plt.xlabel("Number of Dice Remaining")
plt.ylabel("Aggressiveness of Strategy")
plt.xticks(np.arange(8)+1, ("1", "2", "3", "4", "5", "6", "7", "8"))
plt.tight_layout()
plt.show()
"""

def distance(strat1, strat2):
    """
    This functions finds the "distance" (i.e. how many 50's) separate two strategy vectors.
    For example, the strategies [100, 0, 50] and [0, 50, 50] have a distance of 3.
    """
    return int(sum([abs(strat1[i]-strat2[i]) for i in range(8)])/50)

# Comparing the optimal strategy to the strongest strategy from each trial
#mean([compare(thebest, endingStrongest[i]) for i in range(100)])
#hist([compare(thebest, endingStrongest[i]) for i in range(100)])

