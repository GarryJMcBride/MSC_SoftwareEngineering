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


# Population size and mutation rate
""" Population size is based on the small file matrix, and set at 500, when the big matrix file
has been implemented, the population size will increase to around 700-1000 """


population_size = 500


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
    return return_list


#test_sequence = individual_combine(testlist)
#print(test_sequence)


# Swap tests within a test suite
""" This function swaps the tests around after the individual combine function has selected at random. This is to move
around the test in a suite at random for different fitness values."""


def swap_test_suite(testkey):
    new_order = list()
    while len(new_order) == 5:
        new_order = random.shuffle(individual_combine(testkey))
    return new_order


#test_sequence = swap_test_suite(testkey)
#print(test_sequence)


# Population created based on arguments of population size and the testlist.
""" This function creates an empty list called 'population' and adds all elements in the range begining with 1,
to the population size + 1. The population list is then appended by the individual combine function so there is 
now a population of combined tests in a suite"""


def create_population(population_size, testlist,):
    population = list()
    for _ in range(1, population_size + 1):
        population.append(individual_combine(testlist))
    return population


#test_sequence = create_population(population_size, testlist)
#print(test_sequence)


# Selection of random neighbour suite
""" Thie functiin is after the tests in a suite have been randomly swapped, the function will then find another 
combined individual, so later on the two suites can be compared in regards to fitness, and if the fitness is higher,
the newly selected neighbour will replace the first selected suite, and if the fitness is less than the first 
selected suite, the climb will finish with the first selected combination, which is unlikely unless the first suite
has a high fitness value to start with, making the odds of finding another with a higher fitness very unlikely."""


def selection_neighbour(individual_combine):
    select = list()
    while len(select) != 1:
        selectone = random.choice(individual_combine(testkey))
        if selectone not in select:
            select.append(selectone)
    return select


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


#test_sequence = selection_neighbour(individual_combine)
#print(test_sequence)


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
            population = sort_population(population)
            best_solution = population[0]
            generations = generations + 1
            counter = 0
            print("generations", generations, "best individual is", population[0], "with fitness", fitness(population[0], genebank))
        elif fitness(best_solution, genebank) >= fitness(population[0], genebank):
            counter = counter + 1
            population = sort_population(population)
            generations = generations + 1
            print("generations", generations, "best individual is", population[0], "with fitness",
                  fitness(population[0], genebank))


# Random search
""" The random search function picks a random test suite from the individual combine function. This is without functions 
like swapping tests or climbing, it basically picks a solution based on the highest fitness."""


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






