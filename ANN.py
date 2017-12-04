"""
    
ANN
    
    We use two neurons as input:
        1) Horizontal Distance from the bird to the nearest pipe
        2) Vertical Distance from the bird to the nearest pipe
        
    We will use XXX neurons in the hidden layer:
    
    We would have a single neuron as output:
        1) Flap or not flap, which should be to SPACE BUTTON
        
    The idea of my ANN is to optimize the inputs to the optimal [0,0], but playing either with the gravity force or the flapping.
    
    
    
Genetic Algorithm

Heritage: Next generation of birds get the data of the fittest birds
Variation: Generate random birds
Selection: Time of the game as fittness factor

Pick:
-mix fittest with less fitter ones? like 2 parents
-maybe mixing all birds with higher prob. to take fittest in the mix

To create new element:
-Crossover: Take half of each parent?
-Mutation: With Rate of a predefined Mutation Rate we force Variation into the Heritage
    
    Initialize:  One World need more than 1 Bird to increase population. Use several random birds to get variety within the generation.
    
    Selection: Fitness of each Bird is their survival time.
    
    Reproduction: Crossover, Mutation
    

"""

import numpy as np
from neupy import layers
import theano
import theano.tensor as T

class Unit():

    def __init__(self):
        this.network = layers.join(layers.Input(2), layers.Relu(6), layers.Dropout(1),)
        this.fitness = 0;
        this.score = 0;
        this.isWinner = false;

class GeneticAlgorithm():
    
    
    def __init__(self , max_units , top_units):
        
        this.iteration = 1
        this.mutateRate = 1
        this.best_population = 0
        this.best_fitness = 0
        this.best_score = 0
        
        this.max_units = max_units
        this.top_units = top_units
        
        if (this.max_units < this.top_units):
            this.top_units = this.max_units
        
        this.Population = []


    def createPopulation(self):
        # clear existent population
        this.Population = []

        for counter in range(max_units):
            global newUnit
            newUnit = Unit()
            this.Population.append(newUnit)


    def activeBrain(pHorizontal , pVertical , pBird){
        output = this.Population[pBird.Index].train( [ pHorizontal , pVertical ] )
        if (output != 0):
            pBird.flap();


    def evolvePopulation():
        
        Winners = this.selection();
        if (this.mutateRate == 1 && Winners[0].fitness < 0){
            this.createPopulation()
        }







np.random.seed(1)

# randmly initialize our weights with mean 0
# Synapses
syn0 = 2*np.random.random((3,4)) - 1
syn1 = 2*np.random.random((4,1)) - 1

# Training step
for j in range(10000000):

    # Feed forward through layers 0, 1 and 2
    l0 = X
    l1 = nonlin(np.dot(l0,syn0))
    l2 = nonlin(np.dot(l1,syn1))

    # how much did we miss the target value?
    l2_error = Y - l2

    if (j % 10000) == 0:
        print ("Error:" + str(np.mean(np.abs(l2_error))))

    # in what direction is the target value?
    # were we really sure? if so, don't change too much.
    l2_delta = l2_error*nonlin(l2,deriv=True)

    # how much did each l1 value contribute to the l2 error (according to the weights)?
    l1_error = l2_delta.dot(syn1.T)

    # in what direction is the target l1?
    # were we really sure? if so, don't change too much.
    l1_delta = l1_error * nonlin(l1,deriv=True)


    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)
