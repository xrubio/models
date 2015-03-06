
#param should be a data.frame with the following structre
#
# nAgents=100,
# xDim=10,
# yDim=10,
# interactionRadius=1,
# moveDistance=1,
# timeSteps=1000,
# nTraits
# replacementRate
# transmissionType c("Vertical","Encounter","Prestige","Conformist")
# innovationRate
# nRuns

#Example
param<-data.frame(nAgents=round(runif(10,50,500)),replacementRate=0.1,
                  xDim=10,yDim=10,
                  interactionRadius=1,moveDistance=1,
                  timeSteps=5,
                  transmissionType="Encounter",innovationRate=0.01,nTraits=3,
                  nRuns=1)
                  


transmissionExecuter<-function(param,allSteps=FALSE)
{

    runCounter=0
    simpRes=NA
    run=NA
    timeSteps=NA
    
    for (x in 1:nrow(param))
        {
            for (y in 1:param$nRuns[x])
                {
                    tmp<-main(nAgents=param$nAgents[x],
                      xDim=param$xDim[x],yDim=param$yDim[x],
                      interactionRadius=param$interactionRadius[x],
                      moveDistance=param$moveDistance[x],
                      timeSteps=param$timeSteps[x],
                      nTraits=param$nTraits[x],
                      transmissionType=param$transmissionType[x],
                      replacementRate=param$replacementRate[x],
                      innovationRate=param$innovationRate[x],
                      nTraitRange=c(0,1,2,3,4),plotSim=FALSE,verbose=FALSE)
                    runCounter=runCounter+1
                    
                    if (allSteps==TRUE)
                        {
                        run=c(run,rep(runCounter,length(tmp)))
                        simpRes=c(simpRes,tmp)
                        timeSteps=c(timeSteps,1:length(tmp))
                        }
                     if (allSteps==FALSE)
                        {
                        run=c(run,runCounter)
                        simpRes=c(simpRes,tmp[length(tmp)])
                        }
                   }
        }
    
    simpRes=simpRes[-1]
    run=run[-1]
    

    if (allSteps==TRUE)
        {
            timeSteps=timeSteps[-1]
            result=data.frame(run=run,diversity=simpRes,
                nAgents=rep(param$nAgent,param$nRuns*param$timeSteps),
                xDim=rep(param$xDim,param$nRuns*param$timeSteps),
                yDim=rep(param$yDim,param$nRuns*param$timeSteps),
                interactionRadius=rep(param$interactionRadius,param$nRuns*param$timeSteps),
                moveDistance=rep(param$moveDistance,param$nRuns*param$timeSteps),
                timeSteps=timeSteps,
                nTraits=rep(param$nTraits,param$nRuns*param$timeSteps),
                replacementRate=rep(param$replacementRate,param$nRuns*param$timeSteps),
                innovationRate=rep(param$innovationRate,param$nRuns*param$timeSteps))
        }
    
    if (allSteps==FALSE)
        {
            result=data.frame(run=run,diversity=simpRes,
                nAgents=rep(param$nAgent,param$nRuns),
                xDim=rep(param$xDim,param$nRuns),
                yDim=rep(param$yDim,param$nRuns),
                interactionRadius=rep(param$interactionRadius,param$nRuns),
                moveDistance=rep(param$moveDistance,param$nRuns),
                step=rep(param$timeSteps,param$nRuns),
                nTraits=rep(param$nTraits,param$nRuns),
                replacementRate=rep(param$replacementRate,param$nRuns),
                innovationRate=rep(param$innovationRate,param$nRuns))
        }
    
return(result)

}

