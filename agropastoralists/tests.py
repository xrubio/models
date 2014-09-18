#!/usr/bin/python3
import os
import ap
import unittest
import sys

pandoraPath = os.getenv('PANDORAPATH', '/usr/local/pandora')
sys.path.append(pandoraPath+'/bin')
sys.path.append(pandoraPath+'/lib')

from pyPandora import Point2DInt, Config, SizeInt

class TestMyWorld(ap.MyWorld):
    def __init__(self, config):
        ap.MyWorld.__init__( self, config)

class TestSequenceFunctions(unittest.TestCase):
    
    def setUp(self):
        return

    def testDisappearWhenCreatingChildren(self):
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()
        myWorld.run()
        index = Point2DInt(0,0)
        for index._x in range(testConfig.size._width):
            for index._y in range(testConfig.size._height):
                myWorld.setValue('ground', index, ap.cellTypes.eWater)

        myWorld.setValue('ground', Point2DInt(0,0), ap.cellTypes.eDune)
        myWorld.setValue('ground', Point2DInt(0,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,0), ap.cellTypes.eInterdune)
        
        myAP = ap.AP('ap_0')
        myWorld.addAgent(myAP)
        
        myAP._population[0] =-1
        myAP._population[1] =-1
        myAP._population.append(20)
        myAP2 = ap.AP('ap_1')
        myWorld.addAgent(myAP2)
        myAP2._population[0] =-1
        myAP2._population[1] =-1
        myAP2._population.append(20)

        myAP.createAgent(2)
        
        self.assertEqual(myAP.getNumberOfIndividuals(),0)
        self.assertEqual(myAP2.getNumberOfIndividuals(),0)
    
    def testSearchSuitableHome(self):
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()
        myWorld.run()

        index = Point2DInt(0,0)        
        for index._x in range(testConfig.size._width):
            for index._y in range(testConfig.size._height):
                myWorld.setValue('ground', index, ap.cellTypes.eWater)
    
        myWorld.setValue('ground', Point2DInt(0,0), ap.cellTypes.eDune)
        myWorld.setValue('ground', Point2DInt(0,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,0), ap.cellTypes.eInterdune)

        myAP = ap.AP('ap_0')
        myWorld.addAgent(myAP)
        myWorld._yearRainfall = 444.0
        myWorld.updateCalories()
        myAP.searchSuitableHome()
        self.assertEqual(myAP.position._x,0)
        self.assertEqual(myAP.position._y,0)
        
        self.assertEqual(len(myAP._plots), 1)
        
    def testDisappearNotPlot(self):
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()

        myAP = ap.AP('ap_0')
        myWorld.addAgent(myAP)
        
        index = Point2DInt(0,0)  
        for index._x in range(testConfig.size._width):
            for index._y in range(testConfig.size._height):
                myWorld.setValue('ground', index, ap.cellTypes.eDune)

        myAP.position = myWorld.getRandomDune()
        myWorld.run()
        reference = myWorld.getAgent('ap_0')
        self.assertEqual(reference, None)
        
    def testResources(self):    
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()
        myWorld.run()

        index = Point2DInt(0,0)
        for index._x in range(testConfig.size._width):
            for index._y in range(testConfig.size._height):
                myWorld.setValue('ground', index, ap.cellTypes.eDune)

        myWorld.setValue('ground', Point2DInt(0,0), ap.cellTypes.eDune)
        myWorld.setValue('ground', Point2DInt(0,1), ap.cellTypes.eInterdune)

        myWorld.changeState(Point2DInt(0,1), ap.cellState.eField)
        
        myWorld._yearRainfall = 0.0001
        myWorld.updateCalories()
        self.assertEqual(myWorld.getValue('calories', Point2DInt(0,1)), 0)
        
        myWorld._yearRainfall = 444.0
        myWorld.updateCalories()
        self.assertTrue(abs(myWorld.getValue('calories', Point2DInt(0,1))-2703780)<10000)
    
    def testStarvation(self):
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()
        myWorld.run()

        index = Point2DInt(0,0)
        for index._x in range(testConfig.size._width):
            for index._y in range(testConfig.size._height):
                myWorld.setValue('ground', index, ap.cellTypes.eDune)
    
        myWorld.setValue('ground', Point2DInt(0,0), ap.cellTypes.eDune)
        myWorld.setValue('ground', Point2DInt(0,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,0), ap.cellTypes.eInterdune)
        
        myAP = ap.AP('ap_0')
        myWorld.addAgent(myAP)
        myAP.position = myWorld.getRandomDune()

        myWorld._yearRainfall = 0
        myWorld.updateCalories()
        myAP.updateState()
        reference = myWorld.getAgent('ap_0')
        self.assertEqual(reference, None)
    
    def testSurvival(self): 
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()
        myWorld.run()
    
        index = Point2DInt(0,0)
        for index._x in range(testConfig.size._width):
            for index._y in range(testConfig.size._height):
                myWorld.setValue('ground', index, ap.cellTypes.eDune)
    
        myWorld.setValue('ground', Point2DInt(0,0), ap.cellTypes.eDune)
        myWorld.setValue('ground', Point2DInt(0,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,0), ap.cellTypes.eInterdune)

        myAP = ap.AP('ap_0')
        myWorld.addAgent(myAP)
        myAP.position = myWorld.getRandomDune()
        
        myWorld._yearRainfall = 444
        myAP.searchSuitableHome()
        
        myWorld.updateCalories()
        myAP.updateState()
        self.assertEqual(myAP._starvationRate, 0)
            
    def testSurvivalNewPlot(self):  
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()
    
        index = Point2DInt(0,0)
        for index._x in range(testConfig.size._width):
            for index._y in range(testConfig.size._height):
                myWorld.setValue('ground', index, ap.cellTypes.eDune)
    
        myWorld.setValue('ground', Point2DInt(0,0), ap.cellTypes.eDune)
        myWorld.setValue('ground', Point2DInt(0,1), ap.cellTypes.eDune)
        myWorld.setValue('ground', Point2DInt(1,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,0), ap.cellTypes.eInterdune)


        myAP = ap.AP('ap_0')
        myWorld.addAgent(myAP)
        myAP.position = myWorld.getRandomDune()
        
        myWorld._yearRainfall = 444.0
        myWorld.updateCalories()
        myWorld.increaseYearsUsed() 
        myAP.searchSuitableHome()
        myAP.manageFarmActivities()

        plot = Point2DInt(myAP._plots[0]._x, myAP._plots[0]._y)
        self.assertEqual(plot._y, myAP._plots[0]._y)
        self.assertTrue(myAP._starvationRate < 1)

        myWorld.updateCalories()
        myWorld.increaseYearsUsed()
        myAP.manageFarmActivities()
    
        myWorld.updateCalories()
        myWorld.increaseYearsUsed()
        myAP.manageFarmActivities()
    
        self.assertNotEqual(plot._y, myAP._plots[0]._y)
        self.assertNotEqual(-1, myAP._plots[0]._y)
        self.assertTrue(myAP._starvationRate < 1)   

        myWorld.updateCalories()
        myWorld.increaseYearsUsed() 
        myAP.updateState()  
        
        self.assertNotEqual(plot._y, myAP._plots[0]._y)
        self.assertNotEqual(-1, myAP._plots[0]._y)
        self.assertTrue(myAP._starvationRate < 1)
    
    def testCaloriesPerAge(self):
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()

        myAP = ap.AP('ap_0')
        myAP._population.append(2)
        myAP._population.append(5)
        myAP._population.append(10)
        myAP._population.append(13)
        myWorld.addAgent(myAP)
    
        self.assertTrue(abs(myAP.getNeededCalories()-9175.9*365.0) < 50.0)
        myWorld.run()
        
    def testNumberOfPlotsNeeded(self):  
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()
        myWorld.run()

        index = Point2DInt(0,0)
        for index._x in range(testConfig.size._width):
            for index._y in range(testConfig.size._height):
                myWorld.setValue('ground', index, ap.cellTypes.eDune)

        myWorld.setValue('ground', Point2DInt(0,0), ap.cellTypes.eDune)
        myWorld.setValue('ground', Point2DInt(0,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,0), ap.cellTypes.eInterdune)
        
        myAP = ap.AP('ap_0')        
        myWorld.addAgent(myAP)
        myAP.position = myWorld.getRandomDune()

        myAP._population.append(2)
        myAP._population.append(5)
        myAP._population.append(10)
        myAP._population.append(13)
        myWorld._yearRainfall = 444.0
        myWorld.updateCalories()
        myWorld.increaseYearsUsed() 

        self.assertEqual(myAP.plotsNeeded(), 2)
        myAP.searchSuitableHome()
        self.assertEqual(len(myAP._plots), 2)
            
    def testAbandonPlots(self):     
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()
        myWorld.run()

        index = Point2DInt(0,0)
        for index._x in range(testConfig.size._width):
            for index._y in range(testConfig.size._height):
                myWorld.setValue('ground', index, ap.cellTypes.eDune)
    
        myWorld.setValue('ground', Point2DInt(0,0), ap.cellTypes.eDune)
        myWorld.setValue('ground', Point2DInt(0,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,0), ap.cellTypes.eInterdune)
            
        myAP = ap.AP('ap_0')        
        myWorld.addAgent(myAP)
        myAP.position = myWorld.getRandomDune()

        myAP._population.append(2)
        myAP._population.append(5)
        myAP._population.append(10)
        myAP._population.append(13)

        myWorld.stepEnvironment()

        myAP._population.pop()
        myAP._population.pop()
        myAP._population.pop()
        myAP._population.pop()
        myAP.searchSuitableHome()
        self.assertEqual(len(myAP._plots), 1)
        
    def testSurplus(self):
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()
        myWorld.run()
    
        index = Point2DInt(0,0)
        for index._x in range(testConfig.size._width):
            for index._y in range(testConfig.size._height):
                myWorld.setValue('ground', index, ap.cellTypes.eDune)
    
        myWorld.setValue('ground', Point2DInt(0,0), ap.cellTypes.eDune)     
        myWorld.setValue('ground', Point2DInt(0,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,0), ap.cellTypes.eInterdune)

        myAP = ap.AP('ap_0')
        myWorld.addAgent(myAP)
        myAP.position = myWorld.getRandomDune()
        
        myWorld._yearRainfall = 444.0
        myWorld.updateCalories()
        myAP.searchSuitableHome()
        myAP.manageFarmActivities()
        self.assertTrue(myAP._surplus> 0)
        
        
        myAP = ap.AP('ap_1')
        myWorld.addAgent(myAP)
        myAP.position = myWorld.getRandomDune()
        
        myWorld._yearRainfall = 50
        myWorld.updateCalories()
        myAP.searchSuitableHome()
        myAP.manageFarmActivities()
        self.assertTrue(myAP._surplus== 0)
        
        myAP = ap.AP('ap_2')
        myWorld.addAgent(myAP)
        myAP.position = myWorld.getRandomDune()
        
        myWorld._yearRainfall = 1100.0
        myWorld.updateCalories()
        myAP.searchSuitableHome()
        myAP.manageFarmActivities()
        self.assertTrue(myAP._surplus== 0)
        
    def testManageAnimals(self):
        myAP = ap.AP('ap_1')
        myAP._animalsProbability = 1.0
        self.assertTrue(myAP._numAnimals== 0)
        
        testConfig = ap.MyWorldConfig('testConfig.xml');
        myWorld = TestMyWorld(testConfig)
        myWorld.initialize()
        myWorld.run()
    
        index = Point2DInt(0,0)
        for index._x in range(testConfig.size._width):
            for index._y in range(testConfig.size._height):
                myWorld.setValue('ground', index, ap.cellTypes.eDune)
    
        myWorld.setValue('ground', Point2DInt(0,0), ap.cellTypes.eDune)     
        myWorld.setValue('ground', Point2DInt(0,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,1), ap.cellTypes.eInterdune)
        myWorld.setValue('ground', Point2DInt(1,0), ap.cellTypes.eInterdune)
        
        myWorld.addAgent(myAP)
        myAP.position = myWorld.getRandomDune()
        
        myAP.manageAnimals()
        myAP.manageAnimals()
        myAP.manageAnimals()
        
        self.assertTrue(myAP._numAnimals== 1)
        

if __name__ == '__main__':
    unittest.main()
