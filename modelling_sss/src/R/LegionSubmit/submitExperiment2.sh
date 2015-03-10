#!/bin/bash -l

# Batch script to run an array job on Legion with the upgraded
# software stack under SGE.

# 1. Force bash
#$ -S /bin/bash

# 2. Request ten minutes of wallclock time (format hours:minutes:seconds).
#$ -l h_rt=0:59:59

# 3. Request 1 gigabyte of RAM.
#$ -l mem=4G

# 4 Request TMPDIR space                                     
#$ -l tmpfs=15G 

# 5. Set up the job array.  In this instance we have requested 10000 tasks
# numbered 1 to 10000.
#$ -t 1-1000

# 6. Set the name of the job.
#$ -N experiment2

# 7. Select the project that this job will run under.
# Find <your_project_id> by running the command "groups"

# 8. Set the working directory to somewhere in your scratch space.  This is
# a necessary step with the upgraded software stack as compute nodes cannot
# write to $HOME.
# Replace "<your_UCL_id>" with your UCL user ID :)
#$ -wd /home/tcrnerc/Scratch/models/ecosociety/temp

# 9. Run the application.
cd $TMPDIR

#export R_SESSION_TMPDIR=$TMPDIR
module unload compilers/intel/11.1/072
module unload mpi/qlogic/1.2.7/intel
module unload mkl/10.2.5/035
module load recommended/r

# 10. Run the script.
# where:
# FOLDERNAME is where the RData are stored
# RFUNCTIONNAME is the name of the R function which calls the simulation
# OUTPUTFOLDERNAME is where the simulation output is stored
# OUTPUTNAME is the name of the output R code
 
Rscript  /home/tcrnerc/Scratch/models/ecosociety/experiment2.R $SGE_TASK_ID
#Rscript  /home/tcrnerc/Scratch/models/<Rscript> $SGE_TASK_ID
#tar zcvf $HOME/Scratch/output/res$SGE_TASK_ID $TMPDIR
#
mv *.RData $HOME/Scratch/output/ecosociety/experiment2/
#mv *.RData $HOME/Scratch/output/<modelN>/<experimentN>
