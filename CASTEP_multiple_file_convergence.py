#!/Users/steven/opt/anaconda3/bin/python3

####################################################################################################
# This code is for working with CASTEP files.
# Steven R. Schofield, University College London, Apr. 2022
####################################################################################################

# Load required packages
import numpy as np

# load main functions
import SRSCastep as cas

######################################################################################################
# Begin Programme
######################################################################################################

# Display programme start message.
cas.startscript()

# Calls a function from SRSCastep module. This searches the .castep file output from a CASTEP job.
# The function cas.getInfoMultipleFiles() can be edited if you need to search for other parameters
# in the .castep file.  Right now it is outputing the cutoff energy, final total enthalpy, and
# a Si-Si bond length (since this was used for a bulk Si cell optimisation with only 2 Si atoms).
# It should be fairly obvious how to edit the module to add or change the search parameters. 
outputData = cas.getInfoMultipleFiles()

# Find the shape of the output data array
numVals, numCategories = outputData.shape

# filename to write
outputFilename = "multiple_file_output.txt"

# write outputfile
myfile = open(outputFilename, "w")
for row in outputData:
    for col in range(numCategories):
        myfile.write('{colentry:15}\t'.format(colentry=row[col]))
    myfile.write('\n')
myfile.close()

# info
print('\nWrote output file',outputFilename,':\n')

myfile = open(outputFilename, "r")
for line in myfile:
    print(line, end='')
myfile.close()
