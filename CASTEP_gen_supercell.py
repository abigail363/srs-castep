#!/Users/steven/opt/anaconda3/bin/python3

####################################################################################################
# This code is for working with CASTEP files.
# Steven R. Schofield, University College London, Apr. 2022
####################################################################################################

# Load required packages
import sys
import numpy as np
import matplotlib.pyplot as plt
import os

# load main functions
import SRSCastep as cas


######################################################################################################
# Begin Programme
######################################################################################################

# Display programme start message.
cas.startscript()

if len(sys.argv) != 5:
    print("Error, expecting one input filename and three integers")
    sys.exit()
    
# Get file name and unit cell multiples from command line options.
filename=str(sys.argv[1])    # filename
aMult = int(sys.argv[2])
bMult = int(sys.argv[3])
cMult = int(sys.argv[4])

# remove extension if present
filename = os.path.splitext(filename)[0]

outfilename = filename+"_out"
# Read in .cell file information
unitcell, elements, coords, cellFileList = cas.readCellDetailed(filename)

# Enlarge the unit cell
a = unitcell[0]
b = unitcell[1]
c = unitcell[2]

a2 = a * aMult
b2 = b * bMult
c2 = c * cMult

unitcell = np.array([a2, b2, c2])

# Create new atomic positions to fill the enlarged unit cell
numAtoms = len(elements)

coordsList = []
elementList = []

coords = coords * [1/aMult, 1/bMult, 1/cMult]

# loop over number of new repititions of the unit cell
for acell in  range(aMult):
    for bcell in range(bMult):
        for ccell in range(cMult):
            elNum = 0
            for xyz in coords:
                coordsList.append(xyz + [acell/aMult, bcell/bMult, ccell/cMult])
                elementList.append(elements[elNum])
                elNum += 1
        
# convert new lists to numpy arrays
coords = np.array(coordsList)
elements = np.array(elementList)

# write the new cell file
cas.writeCellDetailed(outfilename,unitcell,elements,coords,cellFileList)

# read and write the original parameter file with new filename
paramsDict = cas.readParam(filename)
cas.writeParam(outfilename,paramsDict)


