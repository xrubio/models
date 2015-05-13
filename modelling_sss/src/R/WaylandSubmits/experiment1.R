

source("./decisionMaking.R")

cores=5
require(utils)
require(foreach)
require(doParallel)
registerDoParallel(cores=cores)




param<-expand.grid(nAgents=50,
                   dimX=30,dimY=30,
                   resourceGrowthRate=25,maxEnergy=100,energyCost=25,
                   nSteps=1000,decisionType=c("greedy","probabilistic"),
                   memory=FALSE,stringsAsFactors=FALSE,
                   radius=c(1,5,10,15),runs=1:10)

tmp=foreach(i=1:nrow(param),.combine=rbind) %dopar%
{
    print(i)
    tmp=main(nAgents=param$nAgents[i],energyCost=param$energyCost[i],
        maxEnergy=param$maxEnergy[i],resourceGrowthRate=param$resourceGrowthRate[i],
        nSteps=param$nSteps[i],dimX=param$dimX[i],dimY=param$dimY[i],
        memory=param$memory[i],decisionType=param$decisionType[i],
        plot=FALSE,verbose=FALSE,stochastic=FALSE,radius=param$radius[i])
}

save.image("experiment1New.RData")


