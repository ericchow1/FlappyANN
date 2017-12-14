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
    
    
    
    http://neupy.com/apidocs/neupy.algorithms.linear.perceptron.html#neupy.algorithms.linear.perceptron.Perceptron
    input: Delta-X & Delta-Y
    target data: low percentage distance value of

"""

import numpy as np
from neupy import layers,algorithms

class Unit():

    def __init__(self):
        #self.network = algorithms.Momentum(layers.Input(2), layers.Relu(6), layers.Dropout(1),)
        self.network = algorithms.RBM(n_visible=2, n_hidden=1)
        self.fitness = 0;
        self.score = 0;
        self.track = [];
        self.isWinner = False;

    def activeBrain(self, pHorizontal , pVertical):
        data = (pHorizontal , pVertical)
        #self.network.train( [0.9,0.9], epochs=100)
        self.track.append( (pHorizontal,pVertical))
        hidden_states = self.network.visible_to_hidden(data)
        #print (data)
        return (hidden_states)

    def train(self,weight):
        
        self.network.train(self.track,weight)
        hidden_stats = self.network.visible_to_hidden(self.track)
        #print (self.track)
        self.track = []

class GeneticAlgorithm():
    
    
    def __init__(self , max_units , top_units):
        
        self.iteration = 1
        self.mutateRate = 1
        self.best_population = 0
        self.best_fitness = 0
        self.best_score = 0
        
        self.max_units = max_units
        self.top_units = top_units
        
        if (self.max_units < self.top_units):
            self.top_units = self.max_units
        
        self.Population = []


    def createPopulation(self):
        # clear existent population
        self.Population = []

        for counter in range(self.max_units):
            global newUnit
            newUnit = Unit()
            self.Population.append(newUnit)


    def activeBrain2(self, pHorizontal , pVertical , pBird):
        output = self.Population[pBird.Index].train( [ pHorizontal , pVertical ] )
        if (output != 0):
            pBird.flap();

    def activeBrain(self, pHorizontal , pVertical):
        self.network.train( [ pHorizontal , pVertical ] , epochs = 30)
        output =  self.network.predict( [ pHorizontal , pVertical ] )
        self.network.architecture()
        return output


    def evolvePopulation():
        
        Winners = self.selection();
        if (self.mutateRate == 1 and Winners[0].fitness < 0):
            self.createPopulation()

global algo
algo =  GeneticAlgorithm(1,1)
algo.createPopulation()
print (algo.Population[0])






