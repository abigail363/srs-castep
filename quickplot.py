#!/Users/steven/opt/anaconda3/bin/python3

####################################################################################################
# This code is for quickly plotting column data from txt file from the command line
# Steven R. Schofield, University College London, Apr. 2022
####################################################################################################

# Load required packages
import sys
import numpy as np
import matplotlib.pyplot as plt

######################################################################################################
# Begin Programme
######################################################################################################

# Display programme start message.
print('quickplot; SRS 18 May 2022')

if len(sys.argv) != 2:
    print("Error, expecting one input file name.")
    sys.exit()

# Get file name from command line options.
filename=str(sys.argv[1])    # filename
 
# Output to screen
print()
print("Opening "+ filename + " for reading")

# Open file
myfile = open(filename, "r")

dataX = []
dataY = []

header = 'yes'
for line in myfile:
    words = line.split()
    if header == 'yes':
        xLabel = words[0]
        yLabel = words[1]
        header = 'no'
        continue
    dataX.append(float(words[0]))
    dataY.append(float(words[1]))
print("DONE")
print()

dataX = np.array(dataX)
dataY = np.array(dataY)

# Close file
myfile.close()

plt.plot(dataX, dataY,marker='o')
plt.xlabel(xLabel)
plt.ylabel(yLabel)
plt.title(filename)
plt.show()
