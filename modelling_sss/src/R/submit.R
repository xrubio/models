source("./decisionMaking.R")
cores=5
require(utils)
require(foreach)
require(doParallel)
registerDoParallel(cores=cores)
radiusSeq<-1:30
result=foreach(i=1:length(radiusSeq),.combine=rbind) %dopar%
{
    print(i)
    replicate(100,main(nAgents=100,energyCost=25,maxEnergy=100,resourceGrowthRate=25,
                       nSteps=500,dimX=30,dimY=30,memory=FALSE,decisionType=c("greedy"),
                       plot=FALSE,verbose=FALSE,stochastic=FALSE,radius=radiusSeq[i])[500])
}

save.image("experiment1New.RData")
