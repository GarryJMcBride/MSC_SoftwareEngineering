import operator, math, random, numpy
from deap import gp, creator, base, tools, algorithms
import arff


"""
Creating 3 lists for the outputs, inputs and lists of lists for the test suites.
"""


effortMM = list()
inputSet = list()
testSuite = list()


"""
The following method is to read the data file where it goes through each row and then creates an empty list named
'dataLine'. Each variable is stored except for the first variable named ID since it wont be calculated and is only
and an identifier, along with the last numeric value which is the target the calculation is aiming for, so it won't
be included either. This method also takes the last 2 lines and separates them for testing away from the rest of the
data file, the reason for this is to see how the solution works with data alone to see results instead of being included
together like the rest of the lines.
"""


def readFile():
    for row in arff.load('Cost Estimation\\Data\\kemerer.arff'):
        dataLine = list()
        # Separating the rows with row 1 actually being valued with a 0 (0 would in this case be the ID)
        dataLine.append(row[1])
        dataLine.append(row[2])
        dataLine.append(row[3])
        dataLine.append(row[4])
        dataLine.append(row[5])
        dataLine.append(row[6])
        # Adds to the last value from the row (The Effort Value) to the output list (The effortMM list)
        effortMM.append(row[7])
        # Adds to the list with the inputs from a row to the list of lists of inputs
        inputSet.append(dataLine)
    # Remove the last 2 data lines from the input list and add them to the test suite for testing
    for i in range(inputSet.__len__(), inputSet.__len__()-2, -1):
        testSuite.append(inputSet[i-1])
        inputSet.remove(inputSet[i-1])


"""
The following code is for division and adds a value of 1 when a 0 becomes present causing and error, the code will 
change said error (0) to a 1 so the program will not crash.
"""


# Method for safe division by 0 Ensures that a division by 0 doesn't terminate the program
def safeDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1


# Method to change the arg value to radians for the sine function and handle value error
def safeSin(x):
    try:
        return math.sin(math.radians(x))
    except ValueError:
        return 1


# Method to change the arg value to radians for the cosine function and handle value error
def safeCos(x):
    try:
        return math.cos(math.radians(x))
    except ValueError:
        return 1


# Method to handle value error for the logarithm operator
def safeLog(x):
    try:
       return math.log(x)
    except ValueError:
        return 1


# Method to handle overflow error for the exponential function
def safeExp(x):
    try:
        return math.exp(x)
    except OverflowError:
        return 1


"""
The Algorithm function where numbers of attributes is stated and calculation techniques are added so the framework knows
what methods it can use to find a solution. The fitness function and individual are included as well from the creator 
section of the framework, toolbox is also contained in this function.
"""


# Initiate the algorithm
def initialize():
    # The following code creates a primitive set and declares the number of inputs for this data set (6)
    pset = gp.PrimitiveSet("MAIN", 6)
    # The following code adds the addition operator to the list of operators. The 2 specifies the number of values this operator requires
    pset.addPrimitive(operator.add, 2)
    # The following code is the subtract Operator
    pset.addPrimitive(operator.sub, 2)
    # This code is the multiply Operator
    pset.addPrimitive(operator.mul, 2)
    # Division take into consideration division by 0
    pset.addPrimitive(safeDiv, 2)
    # The following code negates a value operator
    pset.addPrimitive(operator.neg, 1)
    # This is the sine function
    pset.addPrimitive(safeSin, 1)
    # This is the cosine function
    pset.addPrimitive(safeCos, 1)
    # Logarithm function
    pset.addPrimitive(safeLog, 1)
    # Exponential
    pset.addPrimitive(safeExp, 1)
    # Ephemeral constant (random number)
    pset.addEphemeralConstant("constant", lambda: random.randint(-500, 500))

    # The following code creates the fitness object with a value -1 because of the minimization problem
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    # The following code creates individuals
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

    # The following code is the toolbox object
    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
    # The following code repeats the creation of individual by repeating the initialization
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)


    def evalSymbReg(individual):
        # The following code is to transform the tree expression in a callable function
        func = toolbox.compile(expr=individual)
        # The following code is to evaluate the mean absolute error between the expression and expected result
        sqerrors = []
        # The following code goes through all the data lists and calculate the module of the difference between the estimated function and the actual function
        for i in range(0, len(inputSet)):
            sqerrors.append(abs(func(*inputSet[i]) - effortMM[i]))
        return math.fsum(sqerrors),

    # The following code sets the evaluate function
    toolbox.register("evaluate", evalSymbReg)
    toolbox.register("select", tools.selTournament, tournsize=50)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=5)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    return toolbox


# Register and average, standard deviation, minimum value and maximum value for the fitness function
def stats(hof):
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)
    return mstats


"""
In this method you are able to change the population, crossover, mutation and the generations the code will run for,
experimentation with changing these rates will be done to see a variety of results. The hall of fame is also present
to narrow down the solutions to the best one.
"""


# The following code is the method to run the full algorithm
def runSymbolicRegression():
    # The following code reads the data file
    readFile()
    # The following code is to initialize the toolbox object
    toolbox = initialize()
    # The following code is to set the population
    pop = toolbox.population(n=450)
    # The following code is to set a hall of fame to save only the 1 best solution
    hof = tools.HallOfFame(1)
    # The following code is to initialize the stats object giving it the best solution as an argument
    mstats = stats(hof)
    # The following code is to call the eaSimple algorithm from the algorithms library
    # it takes population, toolbox, crossover rate, mutation rate, statistics and the best individual
    algorithms.eaSimple(pop, toolbox, 0.9, 0.2, 1500, stats=mstats, halloffame=hof)

    print("Best individual is", hof[0], "with fitness value:", hof[0].fitness)

    # The following code is to make the best expression runnable and evaluate it
    func = toolbox.compile(expr=hof[0])
    # The following code is used to store the mean average error value for the test suite
    testSuiteMAE = 0
    for i in range(0, len(testSuite)):
        testMAE = func(*testSuite[i])
        print("The data line:", testSuite[i], "was used as a test. The estimated effort is:", testMAE)
        testSuiteMAE = testSuiteMAE + testMAE - effortMM[effortMM.__len__()-1-i]
        # Print the last 2 entries of the list of output to use as comparison against the evaluated output
        print("The actual effort is: ", effortMM[effortMM.__len__()-1-i])
    testSuiteMAE = abs(testSuiteMAE)
    print("The mean average error for the test suite is:", testSuiteMAE)
    return pop, stats, hof


runSymbolicRegression()