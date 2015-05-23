#
# Copyright (c) 2015
# COMPUTER APPLICATIONS IN SCIENCE & ENGINEERING
# BARCELONA SUPERCOMPUTING CENTRE - CENTRO NACIONAL DE SUPERCOMPUTACIÓN
# http://www.bsc.es
#
# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# The code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public 
# License along with this code. If not, see <http://www.gnu.org/licenses/>.
# 

library(plyr)    
library(EasyABC)
options(warn=-1)

source('model.R')    
exploreModel <- function(params)
{
    source('model.R')
    set.seed(params[1])
    initMean <- params[2]
    modMean <- params[3]
    # compute initial values
    evidence <- loadEvidence('../data/duration_sieges.csv')
    # run simulation
    durations <- executeSim(initMean, modMean, evidence)
    return(durations)
}

# prior config, initial mean and mod mean
myPrior <- list(c("unif", 10, 40), c("unif", -4, 4))

# observed evidence
evidence <- loadEvidence('../data/duration_sieges.csv')
# order dataset for year then duration 
durations <- evidence[with(evidence, order(iyear, duration)),]$duration

n=100000
# proportion of simulations to be retained (i.e. tolerance level)
p=0.0002
ABC_rej<-ABC_rejection(model=exploreModel, prior=myPrior, nb_simul=n, summary_stat_target=durations, tol=p, n_cluster=4, use_seed=T, verbose=F)

save(ABC_rej, file="results.Rdata")

