#!/bin/bash
#######################################################################################
# Bash script for making castep input files for running on myriad@ucl.
# Steven R. Schofield March 2022
#######################################################################################

# Load the computation variable parameters from the file
source calculation_parameters.txt

# make temporary directory to make the files
mkdir -p temporary

# make directory where jobs will run
mkdir -p rundir

# Copy basis information to rundir
cp JOBS/* temporary

# go into the GJF directory and get list of jobs to run
cd temporary

STRUCTURELIST=$(ls *.cell | sed -n 's/\.cell$//p')

## Create the gaussian job input files (.gjf)
for STRUCTURE in $STRUCTURELIST
do
    echo -n "Making job folder: "
    echo $STRUCTURE
    mkdir -p ../rundir/$STRUCTURE
    cp $STRUCTURE.* ../rundir/$STRUCTURE

    # get list of USP needed
    USPLIST=$(grep usp $STRUCTURE.cell | awk '{print $2}')
    for USP in $USPLIST
    do
	echo "copying pseudopotential "$USP
	cp ../USP/$USP ../rundir/$STRUCTURE
    done
    echo ""
done

echo ""
echo "Now creating the job scripts"
echo ""
# Create a script to launch all jobs
echo "#!/bin/sh" > launch_all.sh

## Create the scheduler batch script
for STRUCTURE in $STRUCTURELIST
do
    SFILENAME="$STRUCTURE.job"
    
    # create gaussian job file (.job) 
    echo "#!/bin/bash -l" > $SFILENAME
    echo >> $SFILENAME
    echo "# Force bash as the executing shell." >> $SFILENAME
    echo "#$ -S /bin/bash" >> $SFILENAME
    echo >> $SFILENAME
    echo "# Request wallclock time (format hours:minutes:seconds)." >> $SFILENAME
    echo "#$ -l h_rt="$WALLCLOCK >> $SFILENAME
    echo >> $SFILENAME
    echo "# Request X gigabyte of RAM per process." >> $SFILENAME
    echo "#$ -l mem="$RAM"G" >> $SFILENAME
    echo >> $SFILENAME
    echo "# Request TMPDIR space per node (default is 10 GB)" >> $SFILENAME
    echo "#$ -l tmpfs="$TMPDIRSPACE"G" >> $SFILENAME
    echo >> $SFILENAME
    echo "# Set the working directory to be the directory the job is submitted from" >> $SFILENAME
    echo "#$ -cwd" >> $SFILENAME
    echo >> $SFILENAME
    echo "# Set the name of the job." >> $SFILENAME
    echo "#$ -N "$STRUCTURE >> $SFILENAME
    echo >> $SFILENAME
    echo "# Merge .e and .o files (error and output)" >> $SFILENAME
    echo "#$ -j y" >> $SFILENAME
    echo >> $SFILENAME
    echo "# Number of processed" >> $SFILENAME
    echo "#$ -pe mpi "$NUMPROC >> $SFILENAME
    echo >> $SFILENAME
    echo "# Setup the CASTEP calculation.  This also creates gaussian environment variables appropriately" >> $SFILENAME
    echo "module unload -f compilers mpi" >> $SFILENAME
    echo "module load mpi/intel/2019/update4/intel" >> $SFILENAME
    echo "module load compilers/intel/2019/update4" >> $SFILENAME
    echo "module load castep/19.1.1/intel-2019" >> $SFILENAME
    #echo "mkdir -p \$GAUSS_SCRDIR" >> $SFILENAME
    echo >> $SFILENAME
    echo "# Run the CASTEP calculation" >>$SFILENAME
    echo "echo -n \"Starting CASTEP calculation: \"" >> $SFILENAME
    echo "date" >> $SFILENAME
    # if it is on myriad then run parallelised version, otherwise run serial version
    if [[ "$HOSTNAME" == *"myriad"* ]]; then
	echo "gerun castep.mpi $STRUCTURE" >> $SFILENAME
    else
	echo "castep.serial $STRUCTURE" >> $SFILENAME
    fi
    echo "echo -n \"Finished: \"" >> $SFILENAME
    echo "date" >> $SFILENAME
    echo >> $SFILENAME
    
    # output to screen the name of the g16 input file just created
    echo "Created the job file "$SFILENAME
    # now add an entry to a launch script
    echo "cd $STRUCTURE" >> launch_all.sh 
    echo "qsub "$SFILENAME >> launch_all.sh
    echo "cd .." >> launch_all.sh
    echo >> launch_all.sh
 
    mv $SFILENAME ../rundir/$STRUCTURE
done

chmod +x launch_all.sh
mv launch_all.sh ../rundir
cd ..

rm -rf temporary

echo ""



