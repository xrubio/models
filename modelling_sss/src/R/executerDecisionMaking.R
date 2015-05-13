

#Example
#param<-data.frame(nAgents=round(runif(10,1,200)),
#                  dimX=30,dimY=30,
#                  resourceGrowthRate=2,maxEnergy=100,energyCost=9,
#                  nSteps=5,decisionType="greedy",memory=TRUE,
#                  nRuns=1,stringsAsFactors=FALSE)



decisionMakingExecuter<-function(param,allSteps=FALSE)
{

    runCounter=0
    nAgentsRes=NA
    run=NA
    nSteps=NA
    pb <- txtProgressBar(min = 1, max = nrow(param), style = 3)
    for (x in 1:nrow(param))
        {
            
            for (y in 1:param$nRuns[x])
                {
                    tmp<-main(nAgents=param$nAgents[x],
                              dimX=param$dimX[x],dimY=param$dimY[x],
                              energyCost=param$energyCost[x],
                              maxEnergy=param$maxEnergy[x],
                              resourceGrowthRate=param$resourceGrowthRate[x],
                              nSteps=param$nSteps[x],
                              memory=param$memory[x],
                              decisionType=param$decisionType[x],
                              radius=param$radius,
                              plot=FALSE,verbose=FALSE)
                    
                    runCounter=runCounter+1
                    
                    if (allSteps==TRUE)
                        {
                        run=c(run,rep(runCounter,length(tmp)))
                        nAgentsRes=c(nAgentsRes,tmp)
                        nSteps=c(nSteps,1:length(tmp))
                        }
                     if (allSteps==FALSE)
                        {
                        run=c(run,runCounter)
                        nAgentsRes=c(nAgentsRes,tmp[length(tmp)])
                        }
                }
            setTxtProgressBar(pb, x)
        }
    close(pb)
    nAgentsRes=nAgentsRes[-1]
    run=run[-1]
    

    if (allSteps==TRUE)
        {
            nSteps=nSteps[-1]
            result=data.frame(run=run,numberOfAgents=nAgentsRes,
                nAgents=rep(param$nAgent,param$nRuns*param$nSteps),
                dimX=rep(param$dimX,param$nRuns*param$nSteps),
                dimY=rep(param$dimY,param$nRuns*param$nSteps),
                energyCost=rep(param$energyCost,param$nRuns*param$nSteps),
                resourceGrowthRate=rep(param$resourceGrowthRate,param$nRuns*param$nSteps),                
                maxEnergy=rep(param$maxEnergy,param$nRuns*param$nSteps),
                decisionType=rep(param$decisionType,param$nRuns*param$nSteps),
                radius=rep(param$radius,param$nRuns*param$nSteps),
                memory=rep(param$memory,param$nRuns*param$nSteps),
                nSteps=nSteps)
        }
    
    if (allSteps==FALSE)
        {
            result=data.frame(run=run,finalNumAgents=nAgentsRes,
                nAgents=rep(param$nAgent,param$nRuns),
                dimX=rep(param$dimX,param$nRuns),
                dimY=rep(param$dimY,param$nRuns),
                energyCost=rep(param$energyCost,param$nRuns),
                resourceGrowthRate=rep(param$resourceGrowthRate,param$nRuns),
                maxEnergy=rep(param$maxEnergy,param$nRuns),               
                decisionType=rep(param$decisionType,param$nRuns),
                radius=rep(param$radius,param$nRuns),
                memory=rep(param$memory,param$nRuns),
                nSteps=rep(param$nSteps,param$nRuns))

        }
    
return(result)

}

