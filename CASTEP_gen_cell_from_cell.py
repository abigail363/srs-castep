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
#params = cas.readParam(readName)

# Read cell file 
unitcell, elements, coords, cellFileList = cas.readCellDetailed(readName)

writename = readName+"_new"
cas.writeCellDetailed(writename,unitcell, elements, coords, cellFileList)
