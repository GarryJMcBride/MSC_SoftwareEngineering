import random


# A Dictionary called 'genebank' where I have separated the data into Keys & Values
"""The small metric file is read using 'r' and recognizing it as a file. Testlist creates an
empty list, where each line in the list has values up until the next 't' and is split up
by the presence of a comma (','). The first element of the line, element 0 is recognized
as the first element between commas beginning with 't', and value 0 (t's) are deleted from
the line and thus they are both recognized as Keys & Values"""


genebank = {}
with open("smallfaultmatrix.txt", "r")as f:
    testlist = list()
    for line in f:
        values = line.strip().split(",")
        testkey = values[0]
        testlist.append(testkey)
        del values[0]
        genebank[testkey] = values
        #print(testkey)


#print(genebank)
#print(genebank.get("t55"))


# Population size and mutation rate
""" Population size is based on the small file matrix, and set at 500, when the big matrix file
has been implemented, the population size will increase to around 700-1000 """
population_size = 500
mutation_rate = 5


# Individual combine with the arguments from the testkey value
"""This function creates an empty list called 'return list' and while the length of the list
is not equal to 5 (for small matrix) and around 50 (for big matrix) then a random choice from the
testkey values (t's) is added to the empty list and combined in a range depending on the file matrix.
If a random choice is not present in the return list, the function adds the combined number of tests
in a suite to the list."""


def individual_combine(testkey):
    return_list = list()
    test = []
    while len(return_list) != 5:
        test = random.choice(testkey)
        if test not in return_list:
            return_list.append(test)
    #for _ in range(5):
        #list.append(random.choice(testkey))
    return return_list


#test_sequence = individual_combine(testlist)
#print(test_sequence)


# Population created based on arguments of population size and the testlist.
""" This function creates an empty list called 'population' and adds all elements in the range begining with 1,
to the population size + 1. The population list is then appended by the individual combine function so there is 
now a population of combined tests in a suite"""


def create_population(population_size, testlist):
    population = list()
    for _ in range(1, population_size + 1):
        population.append(individual_combine(testlist))
    return population

#test_sequence = create_population(population_size, testlist)
#print(test_sequence)


# Fitness function based on the APFD Formula
""" APFD is a float (percentage based) rating instead of an integer (whole number based) which is between 0-1
which takes the randomly selected tests combined into a test suite from the combine function, which finds the number of
of one of the tests in order that finds a fault quicker than the next test, e.g if T1's first element is 0, but the next 
test after T1 is T2, and this test has found a fault, and so on until faults are found, the first number is 2 as that is
the fault found on the second test in the first element, and replaces the missing fault in the first element, in the 
first test. Faults can be found on other tests ranging from however many tests are in the combined suite, in either 
element. All numbers (from finding faults in the tests) are added together and then divided by 5*9 (for small matrix) 
for the fitness value. The code below implements that 1 is greater than 0 towards the 
fitness value, and if 0 is found then go no further."""


def fitness(s, genes):
    total = 0

    for i in range(0, genes[s[0]].__len__()):
        found = False
        for y in range(0, s.__len__()):
           if genes[s[y]][i] == "1":
                total = total + y + 1
                found = True
                break
        if not found:
            total = total + genes[s[0]].__len__()
    value = 1 - (total/(s.__len__()*genes[s[0]].__len__())) + (1/(2*s.__len__()))
    return value


# Population sorted with arguments on population
""" The population is sorted based on the weakest showing first in reverse so the running code with climb
to the highest fitness value from the test suite of randomly chosen tests. A lambda function can take any number of 
arguments, but can only have one expression, this small anonymous function will direct the population to sort in a 
way that is necessary."""


def sort_population(population):
    population = sorted(population, key=lambda x: fitness(x, genebank), reverse=True)
    return population


# Selection function with arguments of population which will select two parents from a combined suite.
""" The function below generates two parents from test suites in the population, named i & j 
both starting from 0 to the length of the population, and uses a while loop to separate j from i when they are equal."""


def selection(population):
    i = random.randint(0, len(population)-1)
    j = random.randint(0, len(population)-1)
    while i == j:
        j = random.randint(0, len(population)-1)
    parent_one = population[i]
    parent_two = population[j]
    return parent_one, parent_two


# The crossover function which will be tied with the selection function in new generation
""" With the arguments of individual one & two, the crossover function, takes i and creates two empty lists names 
child one & child two. J within a range of 0 to i adds a selected child of J to to a child of i and then combines to 
both childs created from the parents in cross over. While loops are added for both child's so that there are no missing 
other halfs of the child's and then breaks when it is the same length as the child it finds."""


def crossover(individualone, individualtwo):
    i = random.randint(0, len(individualone))
    child_one = list()
    child_two = list()
    for j in range(0, i):
        child_one.append(individualone[j])
    for j in range(0, i):
        child_two.append(individualtwo[j])
    while len(child_one) != len(individualone):
        for j in individualtwo:
            if j not in child_one:
                child_one.append(j)
            if len(child_one) == len(individualone):
                break
    while len(child_two) != len(individualtwo):
        for j in individualone:
            if j not in child_two:
                child_two.append(j)
            if len(child_two) == len(individualtwo):
                break
    return child_one, child_two


# A new generation is created with arguments from the population so that the children from the parents are present
""" The function below takes the top 10% from the newly created generation and creates a new population of the top 10.
Two while loops are created so that if the length of the new population is less than the top 10, it adds the children
to the empty list. The second while loop is in case the length of the new population is less than the length of the 
original population, then also add the children from the cross over function to the empty list."""


def new_generation(population):
    top_10 = len(population) // 10
    new_population = list()
    top_10_population = list()
    for i in range(0, top_10):
        top_10_population.append(population[i])
    while len(new_population) < top_10:
        parents = selection(top_10_population)
        parentone = parents[0]
        parenttwo = parents[1]
        children = crossover(parentone, parenttwo)
        new_population.append(children[0])
        new_population.append(children[1])
    while len(new_population) < len(population):
        parents = selection(population)
        parentone = parents[0]
        parenttwo = parents[1]
        children = crossover(parentone, parenttwo)
        new_population.append(children[0])
        new_population.append(children[1])
    return new_population


# The mutation function with arguments of rate and population
""" The individuals in the population (which they are a new generation of children from parents) are created in a list
that has a random choice between 0-100 to mutate the the test suite in the new generation around so that different 
arrays are now created with multiple fitness values in different versions of test suites."""


def mutation(population, mutation_rate):
    for individual in population:
        random_roll = random.choice(range(100))
        if random_roll < mutation_rate:
            random_test = random.randint(0, len(individual)-1)
            test = testlist[random.randint(0, len(testlist)-1)]
            if test not in individual:
                individual[random_test] = test
    return population


# The algorithm function
""" The algorithm brings all the functions together. Crossover and selection are called inside new generation which is
called inside the algorithm. A while loop has been implemented when the counter is less than 100 and if the fitness
from the best solution is less than the fitness of the population the counter ends at 0, then if else the fitness of
the best solution is greater than or equal to the fitness of the population, then the generations are produced and the 
counter if it hasn't found a better solution after a 100 generations stops, e.g if the fitness value stays the same 
after 100 generations it will end."""


def algorithm(population_size):
    population = create_population(population_size, testlist)
    population = sort_population(population)
    generations = 0
    counter = 0
    best_solution = population[0]
    print(generations)
    while counter < 100:
        if fitness(best_solution, genebank) < fitness(population[0], genebank):
            population = new_generation(population)
            population = mutation(population, mutation_rate)
            population = sort_population(population)
            best_solution = population[0]
            generations = generations + 1
            counter = 0
            print("generations", generations, "best individual is", population[0], "with fitness", fitness(population[0], genebank))
        elif fitness(best_solution, genebank) >= fitness(population[0], genebank):
            counter = counter + 1
            population = new_generation(population)
            population = mutation(population, mutation_rate)
            population = sort_population(population)
            generations = generations + 1
            print("generations", generations, "best individual is", population[0], "with fitness",
                  fitness(population[0], genebank))


# Random search
""" The random search function picks a random test suite from the individual combine function. This is without functions 
like mutation or crossover, it basically picks a solution based on the highest fitness."""


def random_search():
    counter = 0
    temp_best = individual_combine(testlist)
    while counter < 10000:
        temp = individual_combine(testlist)
        if fitness(temp_best, genebank) < fitness(temp, genebank):
            temp_best = temp
        counter = counter + 1

    print(temp_best, "with fitness", fitness(temp_best, genebank))


algorithm(population_size)
#random_search()


