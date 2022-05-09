#!/Users/steven/opt/anaconda3/bin/python3

####################################################################################################
# This code is for working with CASTEP files.
# Steven R. Schofield, University College London, Apr. 2022
####################################################################################################

# Load required packages
import sys
import numpy as np
import matplotlib.pyplot as plt

# load main functions
import SRSCastep as cas


######################################################################################################
# Begin Programme
######################################################################################################

# Display programme start message.
cas.startscript()

if len(sys.argv) != 2:
    print("Error, expecting one input file name.")
    sys.exit()

# Get file name from command line options.
filename=str(sys.argv[1])    # filename
 
steps, energy = cas.getInfoSingleFile(filename)

numE = len(energy)

plt.plot(steps, energy,marker='o')
plt.xlabel('Iteration step')
plt.ylabel('Total energy (eV)')
energyStr=str(energy[numE-1])
plotTitle='Total energy convergence: '+energyStr+' eV'
plt.title(plotTitle)
plt.show()
