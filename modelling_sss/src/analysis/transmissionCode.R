
library(ggplot2)

# load batch of csvs and create a single data frame
listOfRuns <- lapply(list.files('../data/tr_numberOfAgents/', full.names=T),read.csv, sep=';')
myData <- do.call('rbind', listOfRuns)

pdf('simpson.pdf', width=20, height=10)
ggplot(myData, aes(x=step, y=simpson, group=factor(run))) + geom_line() + facet_grid(transmissionType~nAgents)
dev.off()

