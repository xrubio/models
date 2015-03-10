#Load Source File
#-the source file is a .RData file where all the functions and codes are preloaded
place<-getwd()
source("/home/tcrnerc/Scratch/models/ecosociety/decisionMaking.R") #load ABM
source("/home/tcrnerc/Scratch/models/ecosociety/executerDecisionMaking.R") #load ABM

setwd(place)#Load Source File

#This allows the definition of arguments (this allows the definition of the random seeds as an input argument)
Args<-commandArgs(TRUE)
set.seed(Args)


param<-data.frame(nAgents=round(runif(1,1,200)),
                  dimX=30,dimY=30,
                  resourceGrowthRate=2,maxEnergy=100,energyCost=9,
                  nSteps=1000,decisionType=rep(c("greedy","probabilistic"),2),memory=c(rep(TRUE,2),rep(FALSE,2)),
                  nRuns=1,stringsAsFactors=FALSE)
                  

res=decisionMakingExecuter(param,allSteps=TRUE)
res$seed=Args
name<-paste("./res",Args,".csv",sep="")
res=data.frame(nAgents=res$nAgents,numberOfAgents=res$numberOfAgents,decisionType=res$decisionType,memory=res$memory,seed=res$seed,run=res$run)
save(res,file=name)

