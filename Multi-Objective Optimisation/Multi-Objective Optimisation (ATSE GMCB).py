"""Importing the necessary packages for the project, such as: the Platypus package with the problem function and the
algorithm needed NSGA-II, Matplob for visualizing the results and numpy for adding support for large, multi-dimensional
arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays."""

from matplotlib import pyplot as plt
from platypus import NSGAII, Problem, Integer
import numpy as np

"""Creating my customer class, I have not used classes before and found it tricky at first but easier for 
creating lists that are relevant to each other. The class includes weighting and requirements."""


class CustomerPurchaser:
    def __init__(self, weighting, requirements):
        self.weighting = weighting
        self.requirements = requirements


#def __init__(weighting, requirements):
#        weighting = weighting()
#        requirements = requirements()


"""Customer requirements created class including the id, value and cost. In class methods, self refers to the 
instance which method was called"""


class CustomerRequirements:
    def __init__(self, id, value, cost):
        self.id = id
        self.value = value
        self.cost = cost


#def __init__(id, value, cost):
#        id = id()
#        value = value()
#        cost = cost()


"""Creating a class to identify the issue with budget and requirements where the cost cannot exceed the profit. 
Minimizing the cost and maximizing the profit using for loops so the model does not fail the stated requirements
of maximizing and minimizing with constraints."""


class ProjectProblem(Problem):
    def __init__(self, requirements, CompBudget):
        super(ProjectProblem, self).__init__(len(requirements), 2)
        self.requirements = requirements
        self.types[:] = Integer(0, 1)
        self.constraints[:] = '<=' + str(CompBudget)
        self.directions[0] = self.MAXIMIZE
        self.directions[1] = self.MINIMIZE

        maximum_value = -1
        maximum_cost = -1

        for req in self.requirements:
            if req.value > maximum_value:
                maximum_value = req.value
            if req.cost > maximum_cost:
                maximum_cost = req.cost

        for req in self.requirements:
            req.value = req.value / maximum_value
            req.cost = req.cost / maximum_cost

    def evaluate(self, solution):
        sum_value = 0
        sum_cost = 0

        for i in range(len(solution.variables) - 1):
            if solution.variables[i] == 1:
                sum_value += solution.problem.requirements[i].value
                sum_cost += solution.problem.requirements[i].cost

        solution.objectives[:] = [sum_value, sum_cost]
        solution.constraints[:] = sum_cost
        solution.evaluated = True


"""Creating a seperate model for the single optimization problem since this project is working with both multiple
and single optimization with the constraints as mentioned above."""


class SingleObjectiveProjectProblem(Problem):
    def __init__(self, requirements, budget, weight):
        super(SingleObjectiveProjectProblem, self).__init__(len(requirements), 1, 1)
        self.requirements = requirements
        self.types[:] = Integer(0, 1)
        self.constraints[:] = '<=' + str(budget)
        self.directions[0] = self.MAXIMIZE
        self.weight = weight

        maximum_value = -1
        maximum_cost = -1

        for req in self.requirements:
            if req.value > maximum_value:
                maximum_value = req.value
            if req.cost > maximum_cost:
                maximum_cost = req.cost

        for req in self.requirements:
            req.value = req.value / maximum_value
            req.cost = req.cost / maximum_cost

    def evaluate(self, solution):
        sum_value = 0
        sum_cost = 0

        for i in range(len(solution.variables) - 1):
            if solution.variables[i] == 1:
                sum_value += solution.problem.requirements[i].value
                sum_cost += solution.problem.requirements[i].cost

        solution.objectives = [(self.weight * sum_value) - ((1 - self.weight) * sum_cost)]
        solution.constraints[:] = sum_cost
        solution.evaluated = True


""" Optimizing multi-objective for the benefit of requirements vs the cost for the problem of the project. A scatter 
plot also produce results for effective comparisons. The iterations is set to 10,000 and will be changed for different 
results to compare.  The scatter plot has been given titles and colours to separate the different optimization results. 
In this case the Mutli-objective is red"""


def multi_objective(requirements, budget):
    problem = ProjectProblem(requirements, budget * sum(req.cost for req in requirements))
    algorithm = NSGAII(problem)
    algorithm.run(10000)

    plt.scatter([s.objectives[0] for s in algorithm.result],
                [s.objectives[1] for s in algorithm.result], color=['#FF0000'], alpha=0.4)
    plt.xlim([min(s.objectives[0] for s in algorithm.result), max(s.objectives[0] for s in algorithm.result)])
    plt.ylim([max(s.objectives[1] for s in algorithm.result), min(s.objectives[1] for s in algorithm.result)])
    plt.xlabel("Customer Value", fontsize=15)
    plt.ylabel("Customer Cost", fontsize=15)
    plt.title('Multi-Objective Result', fontsize=22, fontweight='bold')
    plt.show()
    return algorithm.result


"""Optimizing single-objective for the benefit of requirements vs the cost for the problem of the project. A scatter 
plot also produce results for effective comparisons. The iterations is set to 10,000 and will be changed for different 
results to compare. The scatter plot has been given titles and colours to separate the different optimization results. 
In this case the Single-objective is blue. The single-objective requires for loops to stop issues because of the 
difference in the method."""


def single_objective(requirements, budget):
    weights = np.arange(0.1, 1, 0.05)
    results = []

    for weight in weights:
        problem = SingleObjectiveProjectProblem(requirements, budget * sum(req.cost for req in requirements), weight)
        algorithm = NSGAII(problem)
        algorithm.run(10000)

        results.append(algorithm.result[0:10])

    cost_value_list = []
    for result_list in results:
        for result in result_list:
            sum_value = 0
            sum_cost = 0

            for i in range(0, len(result.variables) - 1):
                if result.variables[i][0]:
                    sum_value += requirements[i].value
                    sum_cost += requirements[i].cost
            cost_value_list.append([sum_value, sum_cost])

    plt.scatter([r[0] for r in cost_value_list], [r[1] for r in cost_value_list], color=['#000080'], alpha=0.4)
    plt.xlim([min(r[0] for r in cost_value_list) - 1, max(r[0] for r in cost_value_list) + 1])
    plt.ylim([max(r[1] for r in cost_value_list) + 1, min(r[1] for r in cost_value_list) - 1])
    plt.xlabel("Customer Value", fontsize=15)
    plt.ylabel("Customer Cost", fontsize=15)
    plt.title('Single-Objective Result', fontsize=22, fontweight='bold')
    plt.show()
    return results


"""Randomly selecting with a random population to select and evaluate solutions for a certain number of iterations for 
the problem of the project. A scatter plot also produce results for effective comparisons. The scatter plot has 
been given titles and colours to separate the different results. In this case the random search is green. The 
random search requires for loops to stop issues because of the difference in the method, keeping the best solutions."""

def random_selection(requirements, budget):
    number_iterations = 100
    results = []

    for i in range(number_iterations):
        problem = ProjectProblem(requirements, budget * sum(req.cost for req in requirements))
        algorithm = NSGAII(problem)
        algorithm.run(1)

        results.append(algorithm.result[0:10])

    cost_value_list = []
    for result_list in results:
        for result in result_list:
            sum_value = 0
            sum_cost = 0

            for i in range(0, len(result.variables) - 1):
                if result.variables[i][0]:
                    sum_value += requirements[i].value
                    sum_cost += requirements[i].cost
            cost_value_list.append([sum_value, sum_cost])

    plt.scatter([r[0] for r in cost_value_list], [r[1] for r in cost_value_list], color=['#006400'], alpha=0.4)
    plt.xlim([min(r[0] for r in cost_value_list) - 1, max(r[0] for r in cost_value_list) + 1])
    plt.ylim([max(r[1] for r in cost_value_list) + 1, min(r[1] for r in cost_value_list) - 1])
    plt.xlabel("Customer Value", fontsize=15)
    plt.ylabel("Customer Cost", fontsize=15)
    plt.title('Random Search Result', fontsize=22, fontweight='bold')
    plt.show()
    return results


"""Getting the customers and requirements from the files from the directories for both files that were set up which
include the requirements and customer value. The for loops consist of finding the maximum value for customer weightings,
normalising the weightings for each customer and finally to get a list of the value and cost of each requirement"""


if __name__ == '__main__':
    customers = []
    costs = []
    requirements = []

    budget = 0.5

    with open('Multi-Objective Optimisation/Classic Data/nrp1_customers', 'r') as customer_file:
        for line in customer_file:
            line_list = line.split()

            customers.append(CustomerPurchaser(int(line_list[0]), line_list[2:]))

    with open('Multi-Objective Optimisation/Classic Data/nrp1_requirements', 'r') as requirements_file:
        costs = requirements_file.readline().split()

    maximum_weight = -1
    for customer in customers:
        if customer.weighting > maximum_weight:
            maximum_weight = customer.weighting

    for customer in customers:
        customer.weighting = customer.weighting / maximum_weight

    for i in range(1, len(costs)):
        value = 0

        for customer in customers:
            if str(i) in customer.requirements:
                value += customer.weighting * (1 / (customer.requirements.index(str(i)) + 1))

        requirements.append(CustomerRequirements(i, value, int(costs[i])))

    multi_objective(requirements, budget)
    single_objective(requirements, budget)
    random_selection(requirements, budget)


"""Finally above we run each of the algorithms for multi-objective, single-objective and random search with the
arguments of requirements and budget."""