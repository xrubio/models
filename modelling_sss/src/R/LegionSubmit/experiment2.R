#Load Source File
#-the source file is a .RData file where all the functions and codes are preloaded
place<-getwd()
source("/home/tcrnerc/Scratch/models/ecosociety/transmission.R") #load ABM
source("/home/tcrnerc/Scratch/models/ecosociety/executerTransmission.R") #load ABM

setwd(place)#Load Source File

#This allows the definition of arguments (this allows the definition of the random seeds as an input argument)
Args<-commandArgs(TRUE)
set.seed(Args)


param<-data.frame(nAgents=round(runif(1,50,500)),replacementRate=0.1,
                  xDim=10,yDim=10,
                  interactionRadius=1,moveDistance=1,
                  timeSteps=5,
                  transmissionType=c("vertical","encounter","prestige","conformist"),
                  innovationRate=0.01,nTraits=3,
                  nRuns=1,stringsAsFactors=FALSE)
                  

res=transmissionExecuter(param,allSteps=FALSE)
res$seed=Args
name<-paste("./res",Args,".csv",sep="")
res=data.frame(transmissionType=res$transmissionType,diversity=res$diversity,nAgents=res$nAgents)
write.csv(res,file=name)

