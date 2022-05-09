#!/Users/steven/opt/anaconda3/bin/python3

####################################################################################################
# This code is for working with CASTEP files.
# Steven R. Schofield, University College London, Apr. 2022
####################################################################################################

####################################################################################################
# This provides a header output when the programme starts
####################################################################################################
def startscript():
  print("CASTEP tools")
  print("Steven R. Schofield (CC-BY Apr 2022) University College London\n")

####################################################################################################
# Reads in a parameter file and returns as python dictionary
####################################################################################################
def readParam(name):
  
  # add the .param extension
  filename = name + ".param"
  
  # Output to screen
  print()
  print("Opening "+ filename)

  # Open file
  myfile = open(filename, "r")

  # Create a dictionary to store the values
  paramsDict = {}
  
  # Loop over the lines of the input file
  for line in myfile:
    # remove all ":" characters
    line = line.replace(":","")
    words = line.split()
    num=(len(words))
    if num >= 2:
      paramsDict[words[0]]=words[1]

  colWidth=max(len(param) for param in paramsDict)

  print()
  for param in paramsDict:
    print('{col1:{width}}  {col2}'.format(col1=param,col2=paramsDict[param],width=colWidth))
  print()
  print()
  
  # Close file
  myfile.close()
  return paramsDict


####################################################################################################
# Writes parameter file
####################################################################################################
def writeParam(name,paramsDict):

  # add the .param extension
  filename = name + ".param"
  
  # Output to screen
  print()
  print("Opening "+ filename +" for writing...")

  # Open file
  myfile = open(filename, "w")

  # Find the longest parameter name
  colWidth=max(len(param) for param in paramsDict)
      
  for param in paramsDict:
    myfile.write('{col1:{width}}  {col2}\n'.format(col1=param,col2=paramsDict[param],width=colWidth))
  print("DONE")
  print()
    
  # Close file
  myfile.close()
  return 

####################################################################################################
# Reads in a cell file and returns as python dictionary
####################################################################################################
def readCell(name):
  
  # add the .param extension
  filename = name + ".cell"
  
  # Output to screen
  print()
  print("Opening "+ filename + " for reading")

  # Open file
  myfile = open(filename, "r")

  cellFileContents = []
  for line in myfile:
    cellFileContents.append(line)

  print("DONE")
  print()
  
  # Close file
  myfile.close()
  
  return cellFileContents



####################################################################################################
# Writes cell file
####################################################################################################
def writeCell(name,cellFileContents):

  # add the .param extension
  filename = name + ".cell"
  
  # Output to screen
  print()
  print("Opening "+ filename +" for writing...")

  # Open file
  myfile = open(filename, "w")
      
  for line in cellFileContents:
    myfile.write(line)
  print("DONE")
  print()
    
  # Close file
  myfile.close()
  return




####################################################################################################
# Get information from .castep output file
####################################################################################################
def getInfoMultipleFiles():
    import os
    import numpy as np
    
    dirList = os.listdir('.')

    castepFileList = []
    for filename in dirList:
        if filename.endswith('.castep'):
            castepFileList.append(filename)
 
    castepFileList.sort()

    # Initialise the lists and at the time define the list headers.
    energyList = ["TotalE(eV)"]
    cutoffList = ["Cutoff(eV)"]
    bondList = ["Bondlength(Ang.)"]
    warningsList = ["Warnings"]
    
    # iterate over all the *.castep files in the directory
    for filename in castepFileList:
        # Open file
        myfile = open(filename, "r")

        # Give the default value in case the search does not find a value in the file.
        # Will crash if this not present and the search fails.
        cutoff = "--"
        finalE = "--"
        bondlength = "--"
        warnings = '--'
        
        # iterate through the lines of the individual .castep file 
        for line in myfile:
            words = line.split()
            numwords = len(words)

            if numwords > 5 and words[2] == 'basis' and words[4] == 'cut-off':
                cutoffE = float(words[6])
            
            if numwords > 3 and words[1] == 'Final' and words[2] == 'Enthalpy':
                finalE = float(words[4])

            if numwords > 5 and words[0] == 'Sge' and words[1] == '1' and words[3] == 'Si':
                bondlength = float(words[6])

            if numwords > 8 and words[0] == '***' and words[6] == 'warnings':
                warnings = int(words[5])

            # This is just output to the screen - show summary of warnings
            # The number of warnings is also written to the output file.
            # These are just checks to make sure we catch any errors.
            if numwords > 0 and words[0] == 'WARNING':
                print(filename+": "+line)

        bondList.append(bondlength)
        energyList.append(finalE)
        cutoffList.append(cutoffE)
        warningsList.append(warnings)
        
        # Close file
        myfile.close()

    # convert final lists to numpy arrays
    cutoffList = np.array(cutoffList)
    energyList = np.array(energyList)
    bondList = np.array(bondList)
    warningsList = np.array(warningsList)

    returnArray = np.transpose([cutoffList,energyList,bondList,warningsList])

    return returnArray



####################################################################################################
# Get information from .castep output file
####################################################################################################
def getInfoSingleFile(filename):
    import os
    import numpy as np
    
    # append extension to filename
    filename = filename+".geom"

    # info
    print("Reading file", filename)
    
    # Open file
    myfile = open(filename, "r")

    # list to store the step number
    stepList = []
    energyList = []

    # counter for the step
    stepcount = 0

    # Toggle for reading energy from the subsequent line to the step number
    readenergy = "no"

    # conversion factor Hartrees to eV
    hartreetoeV = 0.0367493242
    
    # iterate through the lines of the individual .castep file 
    for line in myfile:
        words = line.split()
        numwords = len(words)

        if readenergy == "yes":
                energy=float(words[0])/hartreetoeV
                energyList.append(energy)
                readenergy = "no"
                
        if numwords > 0 and words[0] == str(stepcount):
            stepList.append(stepcount)
            stepcount += 1
            readenergy = "yes"
            
    # Close file
    myfile.close()

    # convert to numpy array
    stepList = np.array(stepList)
    energyList = np.array(energyList)
    
    return stepList, energyList 
