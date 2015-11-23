from fargo2 import rollN
from fargo2 import summarize
from fargo2 import result
from operator import add
from math import factorial
from random import randint
from random import random
import functools
from  nDiceResult import *
#import matplotlib.pyplot as plt

"""
Applying genetic algorithm
Each member of the population should be a (nonincreasing?)
8-vector of multiples of 50 from 50 to 3100.
e.g. the number 800 in the 3rd position of the list means that 
with 3 dice remaining, the function should continue unless the 
score is ABOVE 800.
"""

def myround(x, base = 50):
    """
    round a nunmber to the nearest 50. This function is used in the
    evolve function to round children to the nearest 50.
    """
    return int(base*round(float(x)/base))




def indiv():
    """
    create a member of the Fargo population. Each individual
    should have a reasonabble max and min threshold
    """
    vector = []
    vector.append(randint(9,61)*50) #from 450 to 3050
    vector.append(randint(8,45)*50) #from 400 to 2250
    vector.append(randint(7,43)*50) #from 350 to 2150
    vector.append(randint(6,41)*50) #from 300 to 2050
    vector.append(randint(5,25)*50) #from 250 to 1250
    vector.append(randint(4,23)*50) #from 200 to 1150
    vector.append(randint(3,21)*50) #from 150 to 1050
    vector.append(randint(2,5)*50)  #from 100 to 250
    return vector


def pop(count):
    """
    Create a number of individuals (i.e. a population).
    count: the number of individuals in the population  
    """
    return [ indiv() for x in range(count) ]


conservativeList = [50 for i in range(8)]
aggressiveList = [5000 for i in range(8)]
    
        
def fitFun(individual):
    """
    Use the expected value function from nDiceREsult.py
    This replaces the iterative fitness function from iterateEvolution.py.
    """
    return findEV(ndice = 10, gene = individual)

# fitFun(conservativeList,10)
# fitFun(aggressiveList,10)



def gradePop(pop):
    'Find average fitness for a population.'
    summed = functools.reduce(add, (fitFun(x) for x in pop), 0)
    return summed / (len(pop) * 1.0)

#gradePop([conservativeList, aggressiveList],10)
#gradePop(pop(10), 10)



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

populationSize = 100
generations = 10

retain = 0.25
add_random = 0.02
mutate = 0.01
elite = 0.05
###################################


#Make starting population
p = pop(populationSize)

#Store fitness history
fitness_history = [gradePop(p)]
population_history = [p]

#Run evolution
for i in range(generations):
    p = evolve(pop = p,
               retain = retain,
               add_random = add_random,
               mutate = mutate,
               elite = elite)
    population_history.append(p)
    
    new_population_grade = gradePop(p)
    print (new_population_grade)
    fitness_history.append(new_population_grade)


# Plot progress
#plt.plot(range(generations+1),fitness_history)
#plt.show()


# Population from the last iteration
fittestPop = population_history[-1]


#From the fittest population, find average individual
idealIndiv = [0 for x in range(8)]
for individual in fittestPop:
    for i in range(8):
        idealIndiv[i] += individual[i]
    #print(individual)
idealIndiv = [myround(x/populationSize) for x in idealIndiv]

print(idealIndiv)

