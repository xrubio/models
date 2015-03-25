#!/usr/bin/python3

import transmission, random

def singleRun():  
    params = transmission.Params()
    params.transmissionType = 'prestige'
    params.nAgents = 30
    params.nSteps = 10
    params.output = 'output_tr_0.csv'
    transmission.run(params)

def exploreNumberOfAgents():
    numRuns = 50
    transmissionTypeSweep = ['vertical','encounter','prestige','conformist']
    
    params = transmission.Params()
    params.nSteps = 1000
    totalRuns = 0
    # perform numRuns of each type, randomly sampling from nAgents 10 to 500
    for i in transmissionTypeSweep:
        for j in range(0, numRuns):
            print('run:',totalRuns+1,'of:',numRuns*len(transmissionTypeSweep))
            params.numRun = totalRuns
            params.transmissionType = i
            params.nAgents = random.randint(50,500)
            params.output = 'output_tr_'+str(params.numRun)+'.csv'
            totalRuns += 1
            transmission.run(params)

def multiple():
    numRuns = 30

    params = transmission.Params()
    params.transmissionType = 'prestige'
    params.nAgents = 100
    params.nSteps = 1000
    params.output = 'output_tr_0.csv'

    for j in range(0, numRuns):
        print('run:',j+1,'of:',numRuns)
        params.numRun = j
        params.output = 'output_tr_'+str(j)+'.csv'
        transmission.run(params)

def main():
    exploreNumberOfAgents()

if __name__ == "__main__":
    main()

