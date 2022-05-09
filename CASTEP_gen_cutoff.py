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

# these are the cut-off values to generate input files forcd J
start = 150
end = 500
step = 25

# Get file name from command line options.
readName=str(sys.argv[1])    # First argument on command line; specifies the coordinates in the desired orientation.

# Read parameters from parameter file
params = cas.readParam(readName)

# Read cell file 
cellContents = cas.readCell(readName)

for var in range(start,end,step):
    writeName = readName + "_" + format(var, '04d')
    params['cut_off_energy'] = var
    cas.writeParam(writeName,params)
    cas.writeCell(writeName,cellContents)


