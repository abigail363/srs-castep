#!/Users/steven/opt/anaconda3/bin/python3

####################################################################################################
# This code is for working with CASTEP files.
# Steven R. Schofield, University College London, Apr. 2022
####################################################################################################

# Load required packages
import sys
import numpy as np
import pandas as pd
import os

# load main functions
import SRSCastep as cas


######################################################################################################
# Begin Programme
######################################################################################################

# Display programme start message.
cas.startscript()

if len(sys.argv) != 2:
    print("Error, expecting one input filename")
    sys.exit()
    
# Get file name and unit cell multiples from command line options.
filename=str(sys.argv[1])    # filename

# remove extension if present
filename = os.path.splitext(filename)[0]

# Filename for the new file to be written
outfilename = filename+"_out"

# Read in .cell file information
unitcell, elements, coords, cellFileList = cas.readCellDetailed(filename)

# Create a python data set from the elements and coords numpy arrays
xyzSet = {'Element':elements.tolist(),'X':coords[:,0].tolist(),'Y':coords[:,1].tolist(),'Z':coords[:,2].tolist()}

# Create pandas data frame for the xyz data - this contains the element type and xyz coords together
xyzDF = pd.DataFrame(xyzSet)

# Sort teh DF
xyzDF.sort_values(by=['Element','Z','Y','X'], ascending=True, inplace=True)

# Create a Pandas Excel writer using XlsxWriter as the engine.
#writer = pd.ExcelWriter('xyz.xlsx', engine='xlsxwriter')
#xyzDF.to_excel(writer, sheet_name='Sheet1')
# Close the Pandas Excel writer and output the Excel file.
#writer.save()

coords = xyzDF[['X','Y','Z']].to_numpy()
elements = xyzDF['Element'].to_numpy()

# write the new cell file
cas.writeCellDetailed(outfilename,unitcell,elements,coords,cellFileList)

# read and write the original parameter file with new filename
paramsDict = cas.readParam(filename)
cas.writeParam(outfilename,paramsDict)


