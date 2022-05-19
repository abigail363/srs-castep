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

if len(sys.argv) == 1:
    # get list of .castep files.  
    dirList = os.listdir('.')
    castepFileList = []
    for filename in dirList:
        if filename.endswith('.castep'):
            castepFileList.append(filename)
    if len(castepFileList) == 1:
        filename = castepFileList[0]
    if len(castepFileList) == 0:
        print("Error, no .castep file in this directory")
        sys.exit()
    if len(castepFileList) > 1:
        print("Error, please specify which .castep file from list")
        for filename in castepFileList:
            print(filename)
        sys.exit()

if len(sys.argv) > 2:
    print("Error, expecting only one input filename")

# Get file name from command line options.
if len(sys.argv) == 2:
    filename=str(sys.argv[1])    # filename

# remove extension if present
filename = os.path.splitext(filename)[0]

steps, energy = cas.getTotalEnergyConvergence(filename)

numE = len(energy)

plt.plot(steps, energy,marker='o')
plt.xlabel('Iteration step')
plt.ylabel('Total energy (eV)')
energyStr=str(energy[numE-1])
plotTitle='Total energy convergence: '+energyStr+' eV'
plt.title(plotTitle)
plt.show()
