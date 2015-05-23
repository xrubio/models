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
library(MASS)

loadEvidence <- function(fileName)
{
    evidence <- read.csv(fileName, sep=';', header=T)
    evidence <- na.omit(evidence)

    evidence$idate <- paste(evidence$iyear,evidence$imonth,evidence$iday,sep="/")
    evidence$otdate <- paste(evidence$oyear,evidence$otmonth,evidence$otday,sep="/")
    evidence$cdate <- paste(evidence$cyear,evidence$cmonth,evidence$cday,sep="/")

    evidence$daysInvested <- as.numeric(as.Date(evidence$cdate) - as.Date(evidence$idate))
    evidence$duration <- as.numeric(as.Date(evidence$cdate) - as.Date(evidence$otdate))    
    evidence <- evidence[order(evidence[,"iyear"], evidence[,"duration"]),]
    return(evidence)
}

executeSim <- function(initMean, modMean, evidence)
{
    siegesDuration <- numeric()
    meanValue <- initMean 
    # fit size parameter of the distribution based on evidence and parameter initMean 
    sizeFit <-fitdistr(evidence$duration, "negative binomial", mu=initMean)$estimate[1]

    for(year in seq(0, length(unique(evidence$iyear))-1))
    {
        # sample as many sieges as the number of historical sieges for given year
        numSieges <- nrow(subset(evidence, iyear==min(evidence$iyear)+year))
        # if meanValue is negative than add sieges with duration=0
        if(meanValue<0)
        {
            siegesDuration <- c(siegesDuration, rep(0,numSieges))
        }
        # else sample the negative binomial distribution
        else
        {
            siegesDuration <- c(siegesDuration, sort(rnbinom(numSieges, size=sizeFit, mu=meanValue)))
        }

        # modify mean according to trends
        meanValue <- meanValue + modMean
    }
    return(siegesDuration)
}

