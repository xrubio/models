
# Experiment 1
data<-read.csv("~/github/XaviModels/modelling_sss/src/R/results/experiment1Complete.csv",col.names=c("initialNAgents","nAgents","type","memory","seed"))


p1<-qplot(data = subset(data,type=="greedy"& memory==TRUE), nAgents, diversity)+geom_smooth(method = "loess", size = 1.5) + coord_cartesian(ylim = c(0, 1)) + ggtitle("Vertical") + scale_y_continuous("Simpson's Diversity") 





# Experiment 2
data<-read.csv("~/github/XaviModels/modelling_sss/src/R/results/experiment2Complete.csv",col.names=c("run","type","diversity","nAgents"))

library(ggplot2)
p1<-qplot(data = subset(data,type=="vertical"), nAgents, diversity)+geom_smooth(method = "loess", size = 1.5) + coord_cartesian(ylim = c(0, 1)) + ggtitle("Vertical") + scale_y_continuous("Simpson's Diversity") 
p2<-qplot(data = subset(data,type=="encounter"), nAgents, diversity)+geom_smooth(method = "loess", size = 1.5) + coord_cartesian(ylim = c(0, 1)) + ggtitle("Encounter") + scale_y_continuous("Simpson's Diversity") 
p3<-qplot(data = subset(data,type=="prestige"), nAgents, diversity)+geom_smooth(method = "loess", size = 1.5) + coord_cartesian(ylim = c(0, 1)) + ggtitle("Prestige") + scale_y_continuous("Simpson's Diversity") 
p4<-qplot(data = subset(data,type=="conformist"), nAgents, diversity)+geom_smooth(method = "loess", size = 1.5) + coord_cartesian(ylim = c(0, 1)) + ggtitle("Conformist") + scale_y_continuous("Simpson's Diversity") 
multiplot(p1, p3, p2, p4, cols=2) #see below for multiplot code
