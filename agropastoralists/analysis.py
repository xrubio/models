#!/usr/bin/python3

import sys, random

pandoraDir = '/home/xrubio/workspace/pandoraMaster/'

sys.path.append(pandoraDir+'/pandora/')
sys.path.append(pandoraDir+'/pandora/pyPandora/')

from pyPandora import Simulation, Point2DInt, SimulationRecord, GlobalAgentStats, AgentNum, AgentMean, AgentSum, AgentStdDev, GlobalRasterStats, RasterMean, RasterSum, SizeInt

record = SimulationRecord(1, False)
record.loadHDF5('data/ap.h5', True, True)

agentResults = GlobalAgentStats(';')
agentResults.addAnalysis(AgentNum())
agentResults.addAnalysis(AgentMean('population'))
agentResults.addAnalysis(AgentSum('population'))
"""
agentResults.addAnalysis(AgentMean('starvation rate %'))
agentResults.addAnalysis(AgentMean('number of plots'))
agentResults.addAnalysis(AgentSum('number of animals'))
"""
agentResults.applyTo(record, 'agents.csv', 'ap')

