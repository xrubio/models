
library(ggplot2)
library(gridExtra)    
library(plyr)

computeSd <- function(x)
{
    sdPop <- sd(x$pop)
    return(data.frame(sdPop = sdPop))
}

# load batch of csvs and create a single data frame
listOfRuns <- lapply(list.files('../data/dmp_convergence/', full.names=T),read.csv, sep=';')
# convergence for memory=F and dt=greedy
convergenceData <- do.call('rbind', listOfRuns)

# compute standard deviation
sdValues <- ddply(convergenceData, "step", computeSd)
pdf('convergence.pdf')
g1 <- ggplot(sdValues, aes(x=step, y=sdPop)) + geom_line()
g2 <- ggplot(convergenceData, aes(x=step, y=pop, group=factor(run))) + geom_line(alpha=0.4)
grid.arrange(g1,g2)
dev.off()

# dynamics divided by memory and decision
listOfRuns <- lapply(list.files('../data/dmp_all/', full.names=T),read.csv, sep=';')
# convergence for memory=F and dt=greedy
myData <- do.call('rbind', listOfRuns)

pdf('all.pdf')
ggplot(myData, aes(x=step, y=pop, group=factor(run))) + geom_line(alpha=0.4) + facet_grid(memory~decisionType)
dev.off()

