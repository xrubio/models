#
# Copyright (c) 2015
# Maria Yubero & Xavier Rubio-Campillo
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

library(ggplot2)
library(gridExtra)

myData <- read.csv('data.csv', sep=";", header=T)
myData$orderedPeriod <- factor(myData$period, levels=c("LBA", "EIA"))

eiaL <- subset(myData, period=="EIA" & bank=='left')
eiaR <- subset(myData, period=="EIA" & bank=='right')
lbaL <- subset(myData, period=="LBA" & bank=='left')
lbaR <- subset(myData, period=="LBA" & bank=='right')

# EDA
g1 <- ggplot(myData, aes(x=height)) + geom_density(fill='cadetblue', col='cadetblue4', size=1, alpha=0.8) + facet_grid(bank~orderedPeriod) + xlab('height (m)')+ theme(axis.text.x = element_text(angle = 45, hjust = 1))
g2 <- ggplot(myData, aes(x=slope)) + geom_density(fill='cadetblue', col='cadetblue4', size=1, alpha=0.8) + facet_grid(bank~orderedPeriod) + xlab('slope (degrees)')+ theme(axis.text.x = element_text(angle = 45, hjust = 1))
g3 <- ggplot(myData, aes(x=aspect)) + geom_density(fill='cadetblue', col='cadetblue4', size=1, alpha=0.8) + facet_grid(bank~orderedPeriod) + xlab('aspect (degrees)')+ theme(axis.text.x = element_text(angle = 45, hjust = 1))
g4 <- ggplot(myData, aes(x=acc)) + geom_density(fill='cadetblue', col='cadetblue4', size=1, alpha=0.8) + facet_grid(bank~orderedPeriod) + xlab('accessibility index')+ theme(axis.text.x = element_text(angle = 45, hjust = 1))
g5 <- ggplot(myData, aes(x=los)) + geom_density(fill='cadetblue', col='cadetblue4', size=1, alpha=0.8) + facet_grid(bank~orderedPeriod) + xlab('visibility index')+ theme(axis.text.x = element_text(angle = 45, hjust = 1))
g6 <- ggplot(myData, aes(x=dist)) + geom_density(fill='cadetblue', col='cadetblue4', size=1, alpha=0.8) + facet_grid(bank~orderedPeriod) + xlab('distance to natural corridors (m)')+ theme(axis.text.x = element_text(angle = 45, hjust = 1))

pdf('figure_4.pdf', width=8, height=6)
g1
dev.off()
pdf('figure_5.pdf', width=8, height=6)
g2
dev.off()
pdf('figure_6.pdf', width=8, height=6)
g3
dev.off()
pdf('figure_7.pdf', width=8, height=6)
g4
dev.off()
pdf('figure_8.pdf', width=8, height=6)
g5
dev.off()
pdf('figure_10.pdf', width=8, height=6)
g6
dev.off()

# height
ks.test(lbaR$height, lbaL$height)
ks.test(eiaL$height, lbaL$height)
ks.test(eiaL$height, lbaR$height)
ks.test(eiaR$height, lbaL$height)
ks.test(eiaR$height, lbaR$height)
ks.test(eiaR$height, eiaL$height)

# slope
# spatial comparison
ks.test(lbaR$slope, lbaL$slope)
ks.test(eiaL$slope, lbaL$slope)
ks.test(eiaL$slope, lbaR$slope)
ks.test(eiaR$slope, lbaL$slope)
ks.test(eiaR$slope, lbaR$slope)
ks.test(eiaR$slope, eiaL$slope)

# aspect
ks.test(lbaR$aspect, lbaL$aspect)
ks.test(eiaL$aspect, lbaL$aspect)
ks.test(eiaL$aspect, lbaR$aspect)
ks.test(eiaR$aspect, lbaL$aspect)
ks.test(eiaR$aspect, lbaR$aspect)
ks.test(eiaR$aspect, eiaL$aspect)

# los
ks.test(lbaR$los, lbaL$los)
ks.test(eiaL$los, lbaL$los)
ks.test(eiaL$los, lbaR$los)
ks.test(eiaR$los, lbaL$los)
ks.test(eiaR$los, lbaR$los)
ks.test(eiaR$los, eiaL$los)

# acc
ks.test(lbaR$acc, lbaL$acc)
ks.test(eiaL$acc, lbaL$acc)
ks.test(eiaL$acc, lbaR$acc)
ks.test(eiaR$acc, lbaL$acc)
ks.test(eiaR$acc, lbaR$acc)
ks.test(eiaR$acc, eiaL$acc)

# distance    
ks.test(lbaR$dist, lbaL$dist)
ks.test(eiaL$dist, lbaL$dist)
ks.test(eiaL$dist, lbaR$dist)
ks.test(eiaR$dist, lbaL$dist)
ks.test(eiaR$dist, lbaR$dist)
ks.test(eiaR$dist, eiaL$dist)

