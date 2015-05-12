###############################################################
# ~Decision Making Model~
# by enrico.crema@gmail.com                                       
#                                        
# Parameters:                                       
# decisionType ::: Type of decision, either "greedy" or "probabilistic"
# memory ::: Boolean, whether the agents move based on current state of the system, or their cognitive maps
# dimX ::: x limit of the world
# dimY ::: y limit of the world
# nAgents ::: Number of agents at initialisation                                        
# nSteps ::: Number of timesteps in the model
# resourceGrowthRate ::: Amount increase of resources per timeStep
# maxEnergy ::: maximum possible storable energy. Also maximum possible cell values in the resource scape. 
# energyCost ::: ammount of enegry spent by each agent each timestep.


#nAgents=100;energyCost=25;maxEnergy=100;resourceGrowthRate=20;nSteps=1000;dimX=30;dimY=30;memory=FALSE;decisionType=c("greedy");plot=FALSE;verbose=FALSE;radius=2



main<-function(nAgents=10,energyCost=25,maxEnergy=100,resourceGrowthRate=20,
               nSteps=1000,dimX=30,dimY=30,
               decisionType=c("greedy","probabilistic"),
               plot=TRUE,verbose=TRUE,radius=1)
    {

        resource<-expand.grid(x=1:dimX,y=1:dimY)
        gridDistance<-as.matrix(dist(resource))
        destinations=apply(gridDistance,1,function(x,radius){return(which(x<=radius))}, radius=radius)
        
        population=rep(0,nSteps) #placeholder for recording population size
        resource$energy=round(runif(dimX*dimY,0,maxEnergy))
        resource$maxResource=resource$energy #maximum possible resource value per cell

        
        #initialise agents as a data.frame:
        agents=data.frame(energy=rep(maxEnergy/2,nAgents),address=sample(nrow(resource),size=nAgents,replace=TRUE))


       
                          
        #Start of the actual simulation#
        if(verbose==TRUE){pb <- txtProgressBar(min = 1, max = nSteps, style = 3)}

        for (t in 1:nSteps)
            {

                                        #STEP 1: Observe, Move, and Collect Energy#

                                        #Agents Move
          
                agents$address=sapply(1:nrow(agents),function(x,agents,resource,destinations)
                    {
                        targetEnergies=resource[destinations[[agents$address[x]]],]$energy
                        newDestinations=destinations[[agents$address[x]]][which(targetEnergies==max(targetEnergies))]

                        if(length(newDestinations)>1)
                            {
                                newDestinations=sample(newDestinations,size=1)
                            }
                        return(newDestinations)
                    },agents=agents,resource=resource,destinations=destinations)






                
                                        #agents consume

                newOrder=sample(1:nrow(agents)) 
                agents=agents[newOrder,]  #shuffle agent order

                for (a in 1:nrow(agents))
                    {
                        
                        collection=maxEnergy-agents$energy[a] #max possible collection
                        energyInCell=resource$energy[agents$address[a]] #perceived ammount of energy
                        if(collection>energyInCell)
                            {
                                collection=energyInCell
                                resource$energy[agents$address[a]]=resource$energy[agents$address[a]]-collection
                            }
                        else
                            {
                               resource$energy[agents$address[a]]=resource$energy[agents$address[a]]-collection
                            }
                        agents$energy[a]=collection+agents$energy[a]
                    }
                
              
                #STEP 2: Reproduce#
                if(any(agents$energy==maxEnergy))
                    {
                        mothers=which(agents$energy==maxEnergy)
                        agents[mothers,1]=agents[mothers,1]/2
                        agents<-rbind(agents,agents[mothers,])
                    }

                #STEP 3: Spend Energy#
                agents$energy=agents$energy-energyCost


                #STEP 4: Death#
                if(any(agents$energy<=0))
                    {
                      death=which(agents[,1]<=0)
                      if(length(death)==nrow(agents))
                            {
                                agents=agents[-death,]
                                print("extinction!")
                                return(population)
                            }
                       agents=agents[-death,]                     
                    }

                #STEP 5: Resource Growth#
                                       
                resource$energy=resource$energy+resourceGrowthRate
                index=which(resource$energy-resource$maxResource>0)
                resource$energy[index]=resource$maxResource[index]


                #Record Population Size:
                population[t]=nrow(agents)
                
                #Optional Plot Function#
                if(plot==TRUE)
                    {
                        par(mfrow=c(1,2))
                        plot(1:t,population[1:t],type="l",xlab="time",ylab="population",
                             main=paste("Avg.Energy=",round(mean(agents$energy),2)))
                        image(x=1:dimX,y=1:dimY,z=resource,main=paste("Avg.Resource=",round(mean(resource),2)),zlim=c(0,maxEnergy))
                        points(agents$x,agents$y,pch=20,cex=2)
                    }

                if(verbose==TRUE){setTxtProgressBar(pb, t)}
            }
        if(verbose==TRUE){close(pb)}
        return(population)
    }






#utility functions #
neighbourhood<-function(xcor,ycor,xLimit,yLimit,resourceMatrix,type=c("greedy","probabilistic"))
{
step=c(-1,0,1)
xcor1=xcor+step
ycor1=ycor+step
address=expand.grid(x=xcor1,y=ycor1)
noMove=address[5,]

if(sum((address$x<xLimit[1]|address$x>xLimit[2]),na.rm=TRUE)>0){address[which(address$x<xLimit[1]|address$x>xLimit[2]),]=NA}
if(sum((address$y<yLimit[1]|address$y>yLimit[2]),na.rm=TRUE)>0){address[which(address$y<yLimit[1]|address$y>yLimit[2]),]=NA}


destinationResource=apply(address,1,function(x,y){
    if(!is.na(x[1]))
        {return(y[x[1],x[2]])}
    if(is.na(x[1]))
        return(NA)},y=resourceMatrix)

if (all(destinationResource==0,na.rm=TRUE)) {return(noMove)}
else {

    if(type=="greedy")
        {
            goto=which(destinationResource==max(destinationResource,na.rm=TRUE))
            if(length(goto)>1){goto=sample(goto,size=1)}
            finaladdress=address[goto,]
        }
    if(type=="probabilistic")
        {
            destinationResource[which(is.na(destinationResource))]=0
            goto=sample(1:9,size=1,prob=destinationResource)
            if(length(goto)>1){goto=sample(goto,size=1)}
            finaladdress=address[goto,]
        }
    return(finaladdress)
      }
}



getEnvironmentAndMove<-function(xcor,ycor,xLimit,yLimit,resourceMatrix,myMap,type=c("greedy","probabilistic"))
    {
        step=c(-1,0,1)
        xcor1=xcor+step
        ycor1=ycor+step
        address=expand.grid(x=xcor1,y=ycor1)
        noMove=address[5,]
        if(sum((address$x<xLimit[1]|address$x>xLimit[2]),na.rm=TRUE)>0)
            {address[which(address$x<xLimit[1]|address$x>xLimit[2]),]=NA}
        if(sum((address$y<yLimit[1]|address$y>yLimit[2]),na.rm=TRUE)>0)
            {address[which(address$y<yLimit[1]|address$y>yLimit[2]),]=NA}
        if(any(is.na(address$x))){address=address[-which(is.na(address$x)),]}

        
        for (x in 1:9)
            {
                past=myMap[address[x,1],address[x,2]]
                current=resourceMatrix[address[x,1],address[x,2]]
                if(is.na(past)){myMap[address[x,1],address[x,2]]=current}
                else if (!is.na(past)){myMap[address[x,1],address[x,2]]=c(past+current)/2}
            }
        destinationResource=apply(address,1,function(x,y){return(y[x[1],x[2]])}
           ,y=myMap)
        if (all(destinationResource==0,na.rm=TRUE)){return(list(myMap,noMove))}
        
        else {
        if(type=="greedy")
            {
                goto=which(destinationResource==max(destinationResource,na.rm=TRUE))
                if(length(goto)>1){goto=sample(goto,size=1)}
                finaladdress=address[goto,]
            }
        if(type=="probabilistic")
            {
                destinationResource[which(is.na(destinationResource))]=0
                if (all(destinationResource==0)){} #if all destinations are 0
                
                goto=sample(1:nrow(address),size=1,prob=destinationResource)
                if(length(goto)>1){goto=sample(goto,size=1)}
                finaladdress=address[goto,]
            }
        
        return(list(myMap,finaladdress))
            }
    }
