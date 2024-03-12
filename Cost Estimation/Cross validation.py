import numpy as np
import pandas as pd
from sklearn import metrics
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import operator, math, random, numpy
from deap import gp, creator, base, tools, algorithms
import arff



premierleagueplayers = pd.read_csv("Cost Estimation\\kemerer.arff")


premierleagueplayers = premierleagueplayers.drop(columns=['Name', 'Team', 'Position'])
print(premierleagueplayers)

#Output list
effortMM = list()
#List of lists of input
inputSet = list()
#List of lists of test suite
testSuite = list()

# Method to read the data file
def readFile():
    # Go through each row of data from the data file
    for row in arff.load('Cost Estimation\\Data\\kemerer.arff'):
        #Create an empty list
        dataLine = list()
        #Store each variables except for the first one(ID) and for the last (EffortMM)
        dataLine.append(row[1])
        dataLine.append(row[2])
        dataLine.append(row[3])
        dataLine.append(row[4])
        dataLine.append(row[5])
        dataLine.append(row[6])
        #Adds the last value from the row (The Effort Value) to the output list (The effortMM list)
        effortMM.append(row[7])
        #Add the list with the inputs from a row to the list of lists of inputs
        inputSet.append(dataLine)
    #Remove the last 2 data lines from the input list and add them to the test suite for testing
    for i in range(inputSet.__len__(), inputSet.__len__()-2, -1):
        testSuite.append(inputSet[i-1])
        inputSet.remove(inputSet[i-1])

X = premierleagueplayers.values[:, 8:16]
Y = premierleagueplayers.values[:, 3]


X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.30)


print("Decision Tree")
print("**************************************")
model = DecisionTreeClassifier()
model.fit(X_train, Y_train)
print(model)
predicted = model.predict(X_test)
print(metrics.classification_report(Y_test, predicted))
print(metrics.confusion_matrix(Y_test, predicted))