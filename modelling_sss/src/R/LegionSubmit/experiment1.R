#Load Source File
#-the source file is a .RData file where all the functions and codes are preloaded
place<-getwd()
source("/home/tcrnerc/Scratch/models/ecosociety/decisionMaking.R") #load ABM
source("/home/tcrnerc/Scratch/models/ecosociety/executerDecisionMaking.R") #load ABM

setwd(place)#Load Source File

#This allows the definition of arguments (this allows the definition of the random seeds as an input argument)
Args<-commandArgs(TRUE)
set.seed(Args)


param<-expand.grid(nAgents=50,
                  dimX=30,dimY=30,
                  resourceGrowthRate=25,maxEnergy=100,energyCost=25,
                  nSteps=1000,decisionType=c("greedy","probabilistic"),memory=FALSE,
                  nRuns=1:10,stringsAsFactors=FALSE,
                  radius=c(1,5,10,15))
                  

res=decisionMakingExecuter(param,allSteps=TRUE)
res$seed=Args
name<-paste("./res",Args,".csv",sep="")
res=data.frame(nAgents=res$nAgents,numberOfAgents=res$numberOfAgents,decisionType=res$decisionType,memory=res$memory,seed=Args,steps=res$nSteps)
write.csv(res,file=name)

