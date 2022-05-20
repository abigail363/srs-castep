#!/Users/steven/opt/anaconda3/bin/python3

####################################################################################################
# This code is for working with CASTEP files.
# Steven R. Schofield, University College London, Apr. 2022
####################################################################################################

# Load required packages
import numpy as np
import sys
import os

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

# remove extension if present
readName = os.path.splitext(readName)[0]

# Read parameters from parameter file
params = cas.readParam(readName)

# Read cell file 
unitcell, elements, coords, cellFileList = cas.readCellDetailed(readName)

vacStart = 15
vacEnd = 50
vacSep = 5

zcellOrig = unitcell[2,2]
coordsOrig = coords
 
for zcell in range(vacStart,vacEnd+vacSep,vacSep):

    # new value for the zrange
    unitcell[2,2] = zcell

    # rescale the z fractional coordinates
    coords = coordsOrig*[1,1,zcellOrig/zcell]
    
        
    # write output files
    writeName = readName + "_" + "vac_"+str(zcell)
    cas.writeParam(writeName,params)
    cas.writeCellDetailed(writeName,unitcell,elements,coords,cellFileList)

