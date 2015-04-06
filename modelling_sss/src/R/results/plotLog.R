library(ggplot2)
source("~/github/models/modelling_sss/src/R/results/plotUtility.R")
# Experiment 1
data<-read.csv("~/github/models/modelling_sss/src/R/results/experiment1Complete.csv",col.names=c("id","initialNAgents","nAgents","type","memory","seed","steps"),header=F)

#generate run Number
data$run<-rep(1:400,rep(1000,400))


p1<-ggplot(data = subset(data,type=="greedy"& memory==TRUE),aes(x=steps, y=nAgents, group=run)) + geom_line(aes(group=run)) +ggtitle("Greedy & Memory")
p2<-ggplot(data = subset(data,type=="greedy"& memory==FALSE),aes(x=steps, y=nAgents, group=run)) + geom_line(aes(group=run)) +ggtitle("Greedy & NoMemory")
p3<-ggplot(data = subset(data,type=="probabilistic"& memory==TRUE),aes(x=steps, y=nAgents, group=run)) + geom_line(aes(group=run)) +ggtitle("Probabilistic & Memory")
p4<-ggplot(data = subset(data,type=="probabilistic"& memory==FALSE),aes(x=steps, y=nAgents, group=run)) + geom_line(aes(group=run)) +ggtitle("Probabilistic & NoMemory")

multiplot(p1, p3, p2, p4, cols=2)
dev.print(device=png,"~/github/models/modelling_sss/src/R/results/experiment1_260315.png",width=800,height=600)


# Experiment 2
data<-read.csv("~/github/models/modelling_sss/src/R/results/experiment2Complete.csv",col.names=c("run","type","diversity","nAgents"),header=FALSE)

library(ggplot2)
p1<-qplot(data = subset(data,type=="vertical"), nAgents, diversity)+geom_smooth(method = "loess", size = 1.5) + coord_cartesian(ylim = c(0, 1)) + ggtitle("Vertical") + scale_y_continuous("Simpson's Diversity") 
p2<-qplot(data = subset(data,type=="encounter"), nAgents, diversity)+geom_smooth(method = "loess", size = 1.5) + coord_cartesian(ylim = c(0, 1)) + ggtitle("Encounter") + scale_y_continuous("Simpson's Diversity") 
p3<-qplot(data = subset(data,type=="prestige"), nAgents, diversity)+geom_smooth(method = "loess", size = 1.5) + coord_cartesian(ylim = c(0, 1)) + ggtitle("Prestige") + scale_y_continuous("Simpson's Diversity") 
p4<-qplot(data = subset(data,type=="conformist"), nAgents, diversity)+geom_smooth(method = "loess", size = 1.5) + coord_cartesian(ylim = c(0, 1)) + ggtitle("Conformist") + scale_y_continuous("Simpson's Diversity") 
multiplot(p1, p3, p2, p4, cols=2) #see below for multiplot code
dev.print(device=png,"~/github/models/modelling_sss/src/R/results/experiment2_110315.png",width=800,height=600)


