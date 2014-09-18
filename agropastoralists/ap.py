#!/usr/bin/python3

#
# Copyright (c) 2014
# COMPUTER APPLICATIONS IN SCIENCE & ENGINEERING
# BARCELONA SUPERCOMPUTING CENTRE - CENTRO NACIONAL DE SUPERCOMPUTACIÓN
# http://www.bsc.es
#
# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Cassandra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public 
# License along with this library.  If not, see <http://www.gnu.org/licenses/>.
# 
#

import os, sys
import random
import math
import sys
import xml.etree.ElementTree
import argparse
import logging

pandoraPath = os.getenv('PANDORAPATH', '/usr/local/pandora')
sys.path.append(pandoraPath+'/bin')
sys.path.append(pandoraPath+'/lib')

from pyPandora import Point2DInt, Agent, World, Config, SizeInt

def enum(**enums):
    """ converts a sequence of values to an C++ style enum """
    return type('Enum', (), enums)


cellTypes = enum(eDune=0, eWater=1, eInterdune=2)
cellState = enum(eWild=0, eField=1, eFallow=2)

class AP(Agent):
    newId = 0
    _caloriesPerAnimal = 0
    _locationTries = 0

    def __init__(self, ident):
        Agent.__init__(self, ident)
        self._homeRange = 10
        self._plots = []
        # list of individuals. if value==-1 means that the individual is dead
        # if value != -1 defines the current age of individual
        self._population = []
        self._population.append(15)
        self._population.append(15)
        self._starvationRate = 0
        self._surplus = 0
        self._numAnimals = 0
        self._animalsProbability = 1.0
        self._yearsWithoutAnimals = 0

    def updateState(self):
        if not self.exists:
            return

        if len(self._plots)!=0:
            self.manageFarmActivities()
            self.manageAnimals()
            self.trackDemography()
        else:
            self.agentDisappear()


    def registerAttributes(self):
        self.registerIntAttribute('population')
        self.registerIntAttribute('starvation rate %')
        self.registerIntAttribute('surplus')
        self.registerIntAttribute('number of plots')
        self.registerIntAttribute('number of animals')
        return

    def serialize(self):
        self.serializeIntAttribute('population', self.getNumberOfIndividuals())
        self.serializeIntAttribute('starvation rate %', int(self._starvationRate * 100.0))
        self.serializeIntAttribute('surplus', self._surplus)
        self.serializeIntAttribute('number of plots', len(self._plots))
        self.serializeIntAttribute('number of animals', self._numAnimals)
        return

    def searchSuitableHome(self):
        if len(self._plots) >= self.plotsNeeded():
            # too many plots for needs = abandon last plot added
            while len(self._plots) > self.plotsNeeded():
                abandonedPlot = self._plots.pop()
                self.getWorld().changeState(abandonedPlot, cellState.eFallow)

            return True
        # If no plot inside your homerange geent)t another random dune
        # Do this for a maximum of 10 times. If you don't find it choose the best available option
        locationTries = self._locationTries
        # Local copy of home and plots location
        home = Point2DInt(self.position._x, self.position._y)
        plots = []
        for plot in self._plots:
            plots.append(Point2DInt(plot._x, plot._y))

        while len(plots) < self.plotsNeeded() and locationTries > 0:
            newPlot = self.getWorld().getRandomPlot(home, plots, self._homeRange)
            # If no plot is found getRandomPlot gives -1
            if newPlot._x != -1:
                plots.append(newPlot)
            else:
                home = self.getWorld().getRandomDune()
                plots = []
                locationTries = locationTries - 1

        # remove old plots that will not be used and add plots that were not used before
        if len(plots) > len(self._plots):
            self.position = home
            for oldPlot in self._plots:
                if not oldPlot in plots:
                    self._plots.remove(oldPlot)
                    self.getWorld().changeState(oldPlot, cellState.eFallow)

            for plot in plots:
                if not plot in self._plots:
                    self._plots.append(Point2DInt(plot._x, plot._y))
                    self.getWorld().changeState(plot, cellState.eField)
        # Return True if locationTries is not 0 (if the agent has found a plot)
        return len(self._plots) > 0

    def plotsNeeded(self):
        cropCalories = self.getWorld().computeCropCalories()
        if cropCalories == 0:
            return max(1, len(self._plots))
        numberPlots = int(math.ceil(self.getWorld().config._reserve*self.getNeededCalories() / cropCalories))
        return numberPlots

    def getNumberOfIndividuals(self):
        individuals = 0
        for i in range(len(self._population)):
            if self._population[i] != -1:
                individuals = individuals + 1
        return individuals

    def consumeAnimal(self):
        if self._numAnimals==0:
            return 0
        self._numAnimals = self._numAnimals-1
        return self._caloriesPerAnimal

    def computeStarvationRate(self, harvest):
        totalFood = harvest + self._surplus
        while( self._numAnimals>0 and totalFood < self.getNeededCalories()):
            totalFood = totalFood + self.consumeAnimal()
        self._starvationRate = 1 - (totalFood / self.getNeededCalories())
        self._starvationRate = max(0, self._starvationRate)

    def manageFarmActivities(self):  
        for plot in self._plots:
            if self.getWorld().getValue('yearsUsed', plot) == 2:
                self.getWorld().changeState(plot, cellState.eFallow)
                self._plots.remove(plot)

        self.searchSuitableHome()
        harvest = 0
        for plot in self._plots:
            harvest = harvest + self.getWorld().getValue('calories', plot)

        self.computeStarvationRate(harvest)
        self._surplus = max(0, int(harvest - self.getNeededCalories()))

    def manageAnimals(self):
        """agents get a calories surplus (one adult animal) every 3 years with uniform animalsProbability.
        In bad years they can choose to kill the animals to top up their calories intake"""
        if self._yearsWithoutAnimals >= 2:
            if random.random() < self._animalsProbability:
                self._numAnimals = self._numAnimals + 1
                self._yearsWithoutAnimals = 0
                return
        self._yearsWithoutAnimals = self._yearsWithoutAnimals + 1

    def trackDemography(self):
        for i in range(len(self._population)):
            # If the individual in position i is not alive, ignore it.
            if self._population[i] == -1:
                continue
            if self.mortalityCheck(i) == True:
                self._population[i] = -1
                continue
            # Skip indexes 0 and 1 (parents) and only look for mates in children
            newAgent = False
            if i > 1 and self._population[i] >= 15:
                newAgent = self.createAgent(i)
            if newAgent == False:
                self._population[i] = self._population[i] + 1
        if random.randint(0, 1) == 1 and self._population[0] != -1 and self._population[1] != -1:
            self._population.append(0)

        if self.getNumberOfIndividuals() > 0:
            return
        self.agentDisappear()

    def mortalityCheck(self, i):
        """MortalityCheck =True means the individual at position i dies"""
        if random.random() < self._starvationRate:
            return True
        mortalityProbability = 0.015
        if self._population[i] < 4:
            mortalityProbability = 0.1
        if random.random() < mortalityProbability:
            return True
        return False

    def agentDisappear(self):
        for plot in self._plots:
            self.getWorld().changeState(plot, cellState.eFallow)
        self.remove()

    def getAdultChild(self):
        for i in range(len(self._population)):
            # Skip indexes 0 and 1 (parents) and only look for mates in children
            if i > 1 and self._population[i] >= 15:
                return i
        return -1

    def createAgent(self, index):
        nearAgents = self.getWorld().getNeighboursIds(self, self.getWorld().config.size._width, self._type)
        for i in range(0, len(nearAgents)):
            agentId = nearAgents[i]
            agent = self.getWorld().getAgent(agentId)
            if agent == None or agent == self:
                continue
            mateIndex = agent.getAdultChild()
            if mateIndex != -1:
                # TODO refactor
                newAgent = AP('ap_' + str(AP.newId))
                AP.newId = AP.newId + 1
                self.getWorld().addAgent(newAgent)
                newAgent.position = self.getWorld().getRandomDune()
                if random.randint(0, 1) == 0:
                    newAgent.position = self.position
                else:
                    newAgent.position = agent.position
                # Assign age to new agent
                newAgent._population[0] = self._population[index]
                newAgent._population[1] = agent._population[mateIndex]
                # Remove agents (childrens that formed new agents) from parents
                self._population[index] = -1
                agent._population[mateIndex] = -1
                if agent.getNumberOfIndividuals() == 0:
                    agent.agentDisappear()
                # if there are no available plots the agent is not created
                if not newAgent.searchSuitableHome():
                    newAgent.agentDisappear()
                return True
        return False

    def getNeededCalories(self):
        calories = 0
        yearlyIncrement = (1994.0 - 600.0) / 15.0
        for i in range(len(self._population)):
            if self._population[i] == -1:
                continue
            calories = calories + 365.0 * (600.0 + self._population[i] * yearlyIncrement)
        if calories == 0:
            raise AssertionError('calories of agent: ' + str(self) + ' to 0')
        neededCalories = calories * self.getWorld().config._requiredNeedsPercentage
        return neededCalories

    def __str__(self):
        return 'agent :' + self.id + ' home at: ' + str(self.position) + ' plots: ' + str(
            len(self._plots)) + ' pop:' + str(self.getNumberOfIndividuals())

class MyWorldConfig(Config):
    def __init__(self, xmlFile):
        Config.__init__(self, xmlFile)

        # climate
        self._climateMean = 0
        self._climateSd = 1
        
        # agents
        self._initialPopulation = 0
        self._locationTries = 10
        self._requiredNeedsPercentage = 1.0

        # animals
        self._animalsCaKg = 0
        self._animalsKg = 0

        # crops
        self._cropsKgHa = 0
        self._cropsCaKg = 0
        self._cropsVariability = 0.0
        self._cropsMinRain = 0.0
        self._cropsOptimalRain = 0.0
        self._cropsMaxRain = 0.0
        self._reserve = 1.0

    def loadParams(self):
        
        # climate
        self._climateMean = self.getParamFloat('climate', 'mean')
        self._climateSd = self.getParamFloat('climate', 'sd')
        # agents
        self._initialPopulation = self.getParamInt('agents', 'initialPopulation')
        self._locationTries = self.getParamInt('agents', 'locationTries')
        self._requiredNeedsPercentage = self.getParamFloat('agents', 'requiredNeedsPercentage')
        # animals
        self._animalsCaKg = self.getParamInt('agents/animals', 'caloriesPerKilo')
        self._animalsKg = self.getParamInt('agents/animals', 'kilos')
        # crops
        self._cropsKgHa = self.getParamInt('agents/crops', 'kilosPerHa')
        self._cropsCaKg = self.getParamInt('agents/crops', 'caloriesPerKilo')
        # percentage of theoretical crop that the agent will try to collect
        self._reserve = self.getParamFloat('agents/crops', 'reserve')
        self._cropsVariability = self.getParamFloat('agents/crops', 'variability')
        self._cropsMinRain = self.getParamFloat('agents/crops/neededRain', 'min')
        self._cropsOptimalRain = self.getParamFloat('agents/crops/neededRain', 'optimal')
        self._cropsMaxRain = self.getParamFloat('agents/crops/neededRain', 'max')

class MyWorld(World):
    def __init__(self, config):
        World.__init__(self, config)
        self._climate = Climate(self.config._climateMean, self.config._climateSd)
        self._yearRainfall = 0

    def createRasters(self):
        self.registerDynamicRaster("ground", True)
        self.registerDynamicRaster("groundState", True)
        self.registerDynamicRaster("calories", True)
        self.registerDynamicRaster("yearsUsed", True)

        self.getDynamicRaster("ground").setInitValues(cellTypes.eDune, cellTypes.eInterdune, cellTypes.eWater)
        self.getDynamicRaster("groundState").setInitValues(cellState.eWild, cellState.eFallow, cellState.eWild)
        self.getDynamicRaster("calories").setInitValues(0, 100000000, 0)
        self.getDynamicRaster("yearsUsed").setInitValues(0, 1 + self.config.numSteps, 0)

        index = Point2DInt(0, 0)
        for index._x in range(self.getBoundaries().left, self.getBoundaries().right+1):
            for index._y in range(self.getBoundaries().top, self.getBoundaries().bottom+1):
                cellType = random.randint(cellTypes.eDune, cellTypes.eInterdune)
                self.setValue('ground', index, cellType)

        # first rain is optimal
        self._yearRainfall = self.config._cropsOptimalRain
        self.updateCalories()

    def createAgents(self):
        AP._caloriesPerAnimal = self.config._animalsCaKg * self.config._animalsKg
        AP._locationTries = self.config._locationTries
        for i in range(self.config._initialPopulation):
            myAP = AP('ap_' + str(AP.newId))
            AP.newId = AP.newId + 1
            self.addAgent(myAP)
            myAP.searchSuitableHome()
            myAP.manageFarmActivities()

    def getRandomDune(self):
        candidates = []
        index = Point2DInt(0, 0)       
        for index._x in range(self.getBoundaries().left, self.getBoundaries().right+1):
            for index._y in range(self.getBoundaries().top, self.getBoundaries().bottom+1):
                # TODO preference to vicinity to water body

                if self.getValue('ground', index) == cellTypes.eDune:
                    candidates.append(index.clone())
        index = random.randint(0, len(candidates) - 1)
        return candidates[index]

    def generateRain(self):
        self._yearRainfall = self._climate.getRain()
        logging.info('year: %s rain: %s', self.currentStep, self._yearRainfall)

    def getRandomPlot(self, home, usedPlots, homeRange):
        if not self.checkPosition(home):
            return Point2DInt(-1, -1)
        candidates = []
        index = Point2DInt(0, 0)
        for index._x in range(-homeRange, 1 + homeRange):
            for index._y in range(-homeRange, 1 + homeRange):
                location = Point2DInt(index._x + home._x, index._y + home._y)
                if not self.checkPosition(location):
                    continue
                if location in usedPlots:
                    continue
                if self.getValue('ground', location) == cellTypes.eInterdune:
                    if self.getValue('groundState', location) == cellState.eWild:
                        candidates.append(location.clone())
        if len(candidates) == 0:
            return Point2DInt(-1, -1)
        index = random.randint(0, len(candidates) - 1)
        return candidates[index]

    def changeState(self, location, newState):
        # if newState is the same than old nothing is done
        if self.getValue('groundState', location) == newState:
            raise Exception('changing state when not needed')
            return
        self.setValue('groundState', location, newState)
        self.setValue('yearsUsed', location, 0)
        if newState == cellState.eField:
            self.setValue('calories', location, self.computeCropCalories())
        else:
            self.setValue('calories', location, 0)

    def getPercentageOfOptimalCrop(self):
        """ returns the percentage of an optimal crop that will be collected with current rainFall """
        # if rain out of the interval min-max return 0.6
        if self._yearRainfall <= self.config._cropsMinRain:
            return 0.0
        if self._yearRainfall >= self.config._cropsMaxRain:
            return 0.0

        # value decrease linearly from optimal rain (value 1.0) to min/max rain (value 0.6), and is 0 for the rest of rain values
        #  if rain < optimal value then value = 1 - (optimal-rain)*0.4/(optimal-min)
        if self._yearRainfall < self.config._cropsOptimalRain:
            return 1.0 - (self.config._cropsOptimalRain-self._yearRainfall)*0.4/(self.config._cropsOptimalRain-self.config._cropsMinRain)
        #  if rain > optimal value then value = 1 - (rain-optimal)*0.4/(max-optimal)
        else:
            return 1.0 - (self._yearRainfall-self.config._cropsOptimalRain)*0.4/(self.config._cropsMaxRain-self.config._cropsOptimalRain)

    def computeCropCalories(self):
        """ Calories obtained from one crop cell depend from rainfall and it's a normally distributed
        value based on optimal rainfall and sd = MyWorldConfig._cropsVariability
        This gives a calorie value that includes surplus based on landscape variability"""

        value = self.getPercentageOfOptimalCrop()
        value = random.normalvariate(value, self.config._cropsVariability)
        value = max(0.0, value)
        calories = int(value * self.config._cropsKgHa * self.config._cropsCaKg )
        return calories

    def updateCalories(self):
        cropCalories = self.computeCropCalories()
        index = Point2DInt(0, 0) 
        for index._x in range(self.getBoundaries().left, self.getBoundaries().right+1):
            for index._y in range(self.getBoundaries().top, self.getBoundaries().bottom+1):
                if self.getValue('groundState', index) != cellState.eField:
                    continue
                self.setValue('calories', index, cropCalories)

    def increaseYearsUsed(self):
        index = Point2DInt(0, 0) 
        for index._x in range(self.getBoundaries().left, self.getBoundaries().right+1):
            for index._y in range(self.getBoundaries().top, self.getBoundaries().bottom+1):
                if self.getValue('groundState', index) == cellState.eFallow and self.getValue('yearsUsed', index) == 1:
                    self.changeState(index, cellState.eWild)
                else:
                    newValue = 1 + self.getValue('yearsUsed', index)
                    self.setValue('yearsUsed', index, newValue)

    def stepEnvironment(self):
        self.generateRain()
        self.updateCalories()
        self.increaseYearsUsed()


class Climate():
    def __init__(self, mean, stddev):
        self._alpha = mean / stddev
        self._beta = stddev

    def getRain(self):
        return random.gammavariate(self._alpha, self._beta)


def main():
    parser = argparse.ArgumentParser()
    logging.basicConfig(filename='rain.log', level=logging.INFO)
    parser.add_argument('-x', '--config', default='config.xml', help='config file')
    args = parser.parse_args()

    config = MyWorldConfig(args.config)
    myWorld = MyWorld(config)
    myWorld.initialize()
    myWorld.run()


if __name__ == "__main__":
    main()


