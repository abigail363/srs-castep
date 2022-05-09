#!/Users/steven/opt/anaconda3/bin/python3

####################################################################################################
# This code is for working with CASTEP files.
# Steven R. Schofield, University College London, Apr. 2022
####################################################################################################

# Load required packages
import numpy as np
import sys

# load main functions
import SRSCastep as cas

######################################################################################################
# Begin Programme
######################################################################################################


# Display programme start message.
cas.startscript()

if len(sys.argv) != 2:
    print("Error, expecting one input file name")
    sys.exit()


# Get file name from command line options.
readName=str(sys.argv[1])    # First argument on command line; specifies the coordinates in the desired orientation.

# Read parameters from parameter file
params = cas.readParam(readName)

# Read cell file 
cellContents = cas.readCell(readName)

vacStart = 10
vacEnd = 50
vacSep = 10

for i in range(vacStart,vacEnd,vacSep):
    
    # change value of the vacuum separation
    cellContents = cas.modifyCell(cellContents,"vac",i)

    # write output files
    writeName = readName + "_" + "vac_"+str(i)
    cas.writeParam(writeName,params)
    cas.writeCell(writeName,cellContents)


