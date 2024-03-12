import random

#Section for target, genes, population size & mutation

target = "Hello World!"
genes = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ! '
population_size = 200
mutation_rate = 0.05


#My foundaiton for my strings to be created with a range of 12


def create_string(genes):
    string = ''.join(random.choice(genes) for _ in range(12))
    return string


#Creating my population list and then creating strings with my genes


def createpopulation(population_size, genes):
    population = list()
    for _ in range(1, population_size + 1):
        population.append(create_string(genes))
    return population

#Fitness code for feedback that the engine gets to guide it toward my target


def fitness_test(individual, target):
    fitness = int()
    for x in range(0, 11):
        if individual[x] == target[x]:
            fitness = fitness + 1
    return fitness


#Population fitness for the genes to sort and aim for final target


def sort_population_fitness(population, target):
    population = sorted(population, key=lambda x: fitness_test(x, target), reverse=True)
    return population


#Initializing bestParent to a random sequence of letters.


def selection(population, target):
    parentone = str()
    parenttwo = str()
    #i = random.choice(range(0, 40))
    #j = random.choice(range(0, 40))
    i = 0; j = 1
    parentone = population[i]
    parenttwo = population[j]
    return parentone, parenttwo


def crossover(individualone, individualtwo):
    new_individual_one = str()
    new_individual_two = str()
    new_individual_one = individualone[0:6] + individualtwo[6:12]
    new_individual_two = individualtwo[0:6] + individualtwo[6:12]
    return new_individual_one, new_individual_two


def mutate_string(individual):
    individual.split()
    new_string = list()
    new_char = random.choice(genes)
    index_of_char = random.choice(range(0, 12))
    for x in range(0, 12):
        if x != index_of_char:
            new_string.append(individual[x])
        if x == index_of_char:
            new_string.append(new_char)
    individual = new_string
    individual = ''.join(individual)
    return individual


#I had an issue with my mutate_population because it was mutating but not with random. I changed 'individual' and it stopped changing the cop from the original and it finally started updating


def mutate_population(population, mutation_rate):
    mutate_odds = 100 * mutation_rate
    for individual in population:
        random_roll = random.choice(range(100))
        #random_roll= 3
        if random_roll < int(mutate_odds):
            population[population.index(individual)] = mutate_string(individual)
            # individual = mutate_string(individual)
    return population


def newgeneration(population, target):
    parents = selection(population, target)
    parentone = parents[0]
    parenttwo = parents[1]
    population = population[0:40]
    for x in range(80):
        newpeople = crossover(parentone, parenttwo)
        new_one = newpeople[0]
        new_two = newpeople[1]
        population.append(new_one)
        population.append(new_two)
    return population


def algorithm(target, mutation_rate, genes, population_size):
    population = createpopulation(population_size, genes)
    population = sort_population_fitness(population,target)
    generations = 0
    while population[0] != target:
        if population[0] == target:
            break
        generations = generations + 1
        population = newgeneration(population, target)
        population = mutate_population(population, mutation_rate)
        population = sort_population_fitness(population, target)
        generations = generations + 1
        print("generations", generations, "best individual is", population[0], "with fitness",
            fitness_test(population[0], target))
        if generations == 10000:
            break
    return generations


#Random search to be compared with Algorithm


def random_search(target, popuation_size):
    generation = 0
    while True:
        population = createpopulation(population_size,target)
        if target in population:
            break
        generation = generation + 1
        print(generation)


algorithm(target, mutation_rate, genes,population_size)

#random_search(target, population_size)