#!/usr/bin/python3

import transmission, random

def exploreNumberOfAgents():
    numRuns = 4
    transmissionTypeSweep = ['vertical','encounter','prestige','conformist']
    
    params = transmission.Params()
    totalRuns = 0
    # perform numRuns of each type, randomly sampling from nAgents 10 to 500
    for i in transmissionTypeSweep:
        for j in range(0, numRuns):
            print('run:',totalRuns+1,'of:',numRuns*len(transmissionTypeSweep))
            params.numRun = totalRuns
            params.transmissionType = i
            params.nAgents = random.randint(10,500)
            params.output = 'output_tr_'+str(params.numRun)+'.csv'
            totalRuns += 1
            transmission.run(params)

def main():
    exploreNumberOfAgents()

if __name__ == "__main__":
    main()

