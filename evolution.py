from fargo2 import rollN
from random import randint
from random import random
from operator import add
import matplotlib.pyplot as plt



"""
Applying genetic algorithm

Each member of the population should be a (nonincreasing?)
8-vector of multiples of 50 from 50 to 3100.

e.g. the number 800 in the 3rd position of the list means that 
with 3 dice remaining, the function should continue unless the 
score is ABOVE 800.
"""

def indiv():
    'create a member of the Fargo population.'
    return [randint(1,62)*50 for x in xrange(8)]


def pop(count):
    """
    Create a number of individuals (i.e. a population).
    count: the number of individuals in the population  
    """
    return [ indiv() for x in xrange(count) ]


conservativeList = [50 for i in range(8)]
aggressiveList = [50000 for i in range(8)]

def listTurn(stratList, oldScore = 0):
    """
    simulate a turn in Fargo using a strategy list.
    This function will be used as the main part of the fitness function.
    """
    turnScore = oldScore
    lst = stratList
    dice = 10       # initialize by rolling 10 dice
    score = 0
    cont = 1

    while cont != 0:
        r = rollN(dice)
        score += r['score']
        dice = r['dice']

        if r['score'] == 0:      #No score imporvement => lose and turn over.
            return turnScore     #End the function if lose

        if dice == 0:           #No dice left => win.
            #Call the function again if win.
            cont = 0
            listTurn(lst, oldScore = turnScore + score) 
            

        if score >= lst[dice-1]:
            cont = 0

    return (turnScore + score)    
    

    
        
def fitFun(individual, iterations):
    """
    Determine the fitness of an individual. Higher is better.
    individual: the individual (i.e. list) to evaluate
    iterations: more iterations will yield a more accurate average
    Note that this fitness function is the average over a (hopefully
    large) number of random iterations.
    """
    summed = sum([listTurn(individual) for x in range(iterations)])
    return summed/iterations

# fitFun(conservativeList,10)
# fitFun(aggressiveList,10)



def gradePop(pop, iterations):
    'Find average fitness for a population.'
    summed = reduce(add, (fitFun(x, iterations) for x in pop), 0)
    return summed / (len(pop) * 1.0)

#gradePop([conservativeList, aggressiveList],10)
#gradePop(pop(10), 10)



def evolve(pop, iterations, retain=0.25, add_random=0.02, mutate=0.01):
    """
    Evolve function for Fargo.
    pop: starting population list
    iterations: number of iterations when testing population members
    retain: fraction of population which will parent the next generation
    add_random: fraction of population to be created randomly
    mutate: fraction of population that will  mutate 
    """

    # Sort strongest to weakest
    graded = [ (fitFun(x, iterations), x) for x in pop]
    graded = [ x[1] for x in sorted(graded)]
    graded.reverse()
    
    
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
            individual[pos_to_mutate] = randint(1,62)*50


    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) / 2
            child = male[:half] + female[half:]
            children.append(child)

    parents.extend(children)
    return parents
    
###################################
## IMPORTANT STARTING PARAMATERS ##
###################################

iterations = 10000
populationSize = 5000
generations = 50

retain=0.25 
add_random=0.02 
mutate=0.01
###################################

#Make starting population
p = pop(populationSize)

#Store fitness history
fitness_history = [gradePop(p,100),]
population_history = [p]

#Run evolution
for i in xrange(generations):
    p = evolve(p,iterations, retain, add_random, mutate)
    population_history.append(p)
    
    new_population_grade = gradePop(p,100)
    print (new_population_grade)
    fitness_history.append(new_population_grade)


# Plot progress
plt.plot(range(generations+1),fitness_history)
plt.show()

# Population from the last iteration
fittestPop = population_history[-1]


#From the fittest population, find average individual
idealIndiv = [0 for x in range(8)]
for individual in fittestPop:
    for i in range(8):
        idealIndiv[i] += individual[i]
    #print(individual)
idealIndiv = [x/populationSize for x in idealIndiv]

print(idealIndiv)
