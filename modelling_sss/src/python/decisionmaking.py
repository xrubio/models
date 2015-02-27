#!/usr/bin/python3

import random, math

def enum(**enums):
    """ converts a sequence of values to an C++ style enum """
    return type('Enum', (), enums)

DecisionType = enum(eGreedy=0, eProb=1)    

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, pos):
        diffX = self.x-pos.x
        diffY = self.y-pos.y
        return math.sqrt(diffX*diffX+diffY*diffY)

    def __str__(self):
        return(str(self.x)+'/'+str(self.y))

class BaseAgent:
    # static attributes
    # energy threshold for reproduction
    maxEnergy = 0
    # map of resources
    resources = None 
    # amount of energy spent by step
    energyCost = 1
    decisionType = DecisionType.eGreedy

    agents = None
    newAgents = None

    def __init__(self, pos, initEnergy):
        self.pos = pos
        self.energy = int(initEnergy)

    def move(self, resourceMap):
        if self.decisionType == DecisionType.eGreedy:
            self.moveGreedy(resourceMap)
        else:
            self.moveProb(resourceMap)

    def moveGreedy(self, resourceMap):
        candidates = list()
        maxValue = 0
        for i in range(self.pos.x-1, self.pos.x+2):
            for j in range(self.pos.y-1, self.pos.y+2):
                candidate = Position(i,j)
                # if not inside boundaries skip
                if not resourceMap.isInside(candidate):
                    continue
                # greedy agent
                newValue = resourceMap.getValue(candidate)
                if newValue<maxValue:
                    continue
                elif newValue==maxValue:
                    candidates.append(candidate)
                else:
                    maxValue = newValue
                    candidates = []
                    candidates.append(candidate)
        random.shuffle(candidates)
        self.pos = candidates[0]

    def sample(self, values):
        samplingValues = list()
        # for each value add as much samplingValues as the number
        for i in range(0,len(values)):
            for j in range(0,values[i]):
                samplingValues.append(i)
        return random.sample(samplingValues,1)[0]

    def moveProb(self, resourceMap):
        values = list()
        candidates = list()
        for i in range(self.pos.x-1, self.pos.x+2):
            for j in range(self.pos.y-1, self.pos.y+2):  
                candidate = Position(i,j)
                # if not inside boundaries skip
                if not resourceMap.isInside(candidate):
                    continue
                candidates.append(candidate)
                values.append(resourceMap.getValue(candidate))
        # if there is no energy in any cell random move
        if sum(values)==0:
            random.shuffle(candidates)
            self.pos = candidates[0]
            return
        index = self.sample(values)
        self.pos = candidates[index]

    def collectEnergy(self):
        # maximum amount of energy that can be collected from a cell without going beyond maxEnergy
        energyInCell = self.resources.getValue(self.pos)
        collected = int(min(energyInCell, self.maxEnergy - self.energy))
        self.resources.setValue(self.pos, self.resources.getValue(self.pos) - collected)
        self.energy += collected

    def clone(self):
        # energy must be maxEnergy for cloning
        if self.energy < self.maxEnergy:
            return
        child = BaseAgent(self.pos, int(self.energy/2))
        self.energy -= child.energy
        BaseAgent.newAgents.append(child)

    def spendEnergy(self):
        self.energy -= self.energyCost

    def checkDeath(self):
        if self.energy <= 0:
            self.agents.remove(self)

    def step(self):
        self.move(self.resources)
        self.collectEnergy()
        self.clone()
        self.spendEnergy()
        self.checkDeath()

    def __str__(self):
        content = 'agent pos:'+str(self.pos)+' energy:'+str(self.energy)
        return(content)


class MemoryAgent(BaseAgent):
    def __init__(self, pos, initEnergy):
        BaseAgent.__init__(self, pos, initEnergy)
        self.memory = Map(self.resources.xDim, self.resources.yDim)

    def step(self):
        self.updateKnowledge()
        self.move(self.memory)
        self.collectEnergy()
        self.cloneWithMemory()
        self.spendEnergy()
        self.checkDeath()
 
    def cloneWithMemory(self):
        # energy must be maxEnergy for cloning
        if self.energy < self.maxEnergy:
            return
        child = MemoryAgent(self.pos, int(self.energy/2))
        self.energy -= child.energy
        BaseAgent.newAgents.append(child)
        child.memory = self.memory.clone()

    def updateKnowledge(self):
      for i in range(self.pos.x-1, self.pos.x+2):
            for j in range(self.pos.y-1, self.pos.y+2):  
                candidate = Position(i,j)
                if not self.resources.isInside(candidate):
                    continue
                oldValue = self.memory.getValue(candidate)
                currentValue = self.resources.getValue(candidate)
                if oldValue == None:
                    newValue = currentValue
                else:
                    newValue = int((oldValue+currentValue)/2)
                self.memory.setValue(candidate,newValue)

class Map:
    def __init__(self, xDim, yDim):
        self.xDim = xDim
        self.yDim = yDim
        self.values = list()

        for i in range(0,self.xDim):
            newRow = list()
            for j in range(0,self.yDim):
                newRow.append(None)
            self.values.append(list(newRow))

    def clone(self):                
        newMap = Map(self.xDim, self.yDim)
        for i in range(0,self.xDim):
            for j in range(0,self.yDim):
                newMap.values[i][j] = self.values[i][j]
        return newMap           

    def getValue(self, pos):
        return self.values[pos.x][pos.y]

    def setValue(self, pos, value):
        self.values[pos.x][pos.y] = value    

    def isInside(self, pos):
        if pos.x <0 or pos.y < 0:
            return False
        if pos.x>=self.xDim or pos.y>=self.yDim:
            return False
        return True

    def __str__(self):
       output = ''
       for i in range(0,self.xDim):
            for j in range(0,self.yDim):
                output += '['+str(i)+','+str(j)+']='+str(self.values[i][j])+' '
            output += '\n'
       return output

class ResourcesMap(Map):
    def __init__(self, xDim, yDim, maxEnergy, resourceGrowthRate):
        Map.__init__(self, xDim, yDim)
        self.growthRate = resourceGrowthRate     
    
        # create both maps (current and max)
        self.maxValues = list()
        # initialize map of resources
        self.fillValues(maxEnergy)


    def fillValues(self, maxEnergy):
        # create max values
        for i in range(0,self.xDim):   
            newRow = list()
            for j in range(0,self.yDim):
                newRow.append(random.randint(0, maxEnergy))
            self.maxValues.append(newRow)
        # copy
        for i in range(0,self.xDim):
            for j in range(0,self.yDim):
                self.values[i][j] = self.maxValues[i][j]
    
    def step(self):
        for i in range(0,self.xDim):
            for j in range(0,self.yDim):
                # already max capacity, skip
                if self.values[i][j] == self.maxValues[i][j]:
                    continue
                self.values[i][j] += self.growthRate

    def __str__(self):
       output = ''
       for i in range(0,self.xDim):
            for j in range(0,self.yDim):
                output += '['+str(i)+','+str(j)+']='+str(self.values[i][j])+'/'+str(self.maxValues[i][j])+' '
            output += '\n'
       return output


class Params:
    def __init__(self):
        self.numRun = 0
        self.output = 'output_dmp.csv'
        ### agents config
        # base config
        self.nAgents = 1
        self.nSteps = 1000
        # values: greedy, probabilistic
        self.decisionType = 'probabilistic'
        # True or False
        self.memory = True 

        # additional params
        # max energy an agent or a cell can accumulate
        self.maxEnergy = 100
        # energy they consume each cycle
        self.energyCost = 9

        ### environment config
        # dimensions of world
        self.xDim = 30
        self.yDim = 30
        # regeneration for each cell for each time step
        self.resourceGrowthRate = 2

def run(params):
    resources = ResourcesMap(params.xDim, params.yDim, params.maxEnergy, params.resourceGrowthRate)

    BaseAgent.resources = resources
    BaseAgent.maxEnergy = params.maxEnergy
    BaseAgent.energyCost = params.energyCost
    if params.decisionType=='greedy':
        BaseAgent.decisionType = DecisionType.eGreedy
    else:
        BaseAgent.decisionType = DecisionType.eProb
    BaseAgent.agents = list() 
    BaseAgent.newAgents = list() 

    for i in range(0, params.nAgents):
        newPos = Position(random.randint(0,params.xDim-1), random.randint(0,params.yDim-1))
        newAgent = None
        if params.memory:
            newAgent = MemoryAgent(newPos, params.maxEnergy/2)
        else:
            newAgent = BaseAgent(newPos, params.maxEnergy/2)
        BaseAgent.agents.append(newAgent)

    # storage            
    output = open(params.output,'w')
    # header
    output.write('run;memory;decisionType;step;pop\n')

    for i in range(0,params.nSteps):
        #print('step:',i,'num agents:',len(BaseAgent.agents))
        #print(resources)
        random.shuffle(BaseAgent.agents)
        for agent in BaseAgent.agents:
            agent.step()
        # add new agents to agents (children is not executed when created)
        BaseAgent.agents += BaseAgent.newAgents
        BaseAgent.newAgents = list()
        resources.step()
        output.write(str(params.numRun)+';'+str(params.memory)+';'+str(params.decisionType)+';'+str(i)+';'+str(len(BaseAgent.agents))+'\n')
    output.close()      

