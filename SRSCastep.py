#!/Users/steven/opt/anaconda3/bin/python3

####################################################################################################
# This code is for working with CASTEP files.
# Steven R. Schofield, University College London, Apr. 2022
# GNU General Public License v3.0
####################################################################################################

####################################################################################################
# This provides a header output when the programme starts
####################################################################################################
def startscript():
  print("CASTEP tools")
  print("Steven R. Schofield (Apr 2022) University College London\n")

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
# Writes parameter file.
# Takes as input a dictionary file with the parameters to be written and writes the .param file.
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
# Reads in a cell file and returns as list
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
# Reads in a cell file and returns as list
####################################################################################################
def readCellDetailed(name):

  import numpy as np
  
  # add the .param extension
  filename = name + ".cell"
  
  # Output to screen
  print()
  print("Opening "+ filename + " for reading")

  # Open file
  with open(filename, "r") as myfile:
    lines = myfile.readlines()

  # number of lines in the file
  numlines = len(lines)

  # list to hold lines other than unit cell and coordinates
  cellFileList = []
  
  # loop through the file
  i = 0
  while i < numlines:
    words = lines[i].split()
    numwords = len(words)
    
    # beginning of the unit cell definition. Read the three vectors as u, v, w, then combine to unitcell.
    if numwords > 0 and str.upper(words[0]) == '%BLOCK' and str.upper(words[1]) == 'LATTICE_CART':
      i+=1
      words = lines[i].split()
      u = np.array([float(words[0]),float(words[1]),float(words[2])])
      i+=1
      words = lines[i].split()
      v = np.array([float(words[0]),float(words[1]),float(words[2])])
      i+=1
      words = lines[i].split()
      w = np.array([float(words[0]),float(words[1]),float(words[2])])
      i+=2 # this skips the %endblock statement
      unitcell = np.array([u,v,w])

    # read atomic coords (fractional)
    if numwords > 0 and str.upper(words[0]) == '%BLOCK' and str.upper(words[1]) == 'POSITIONS_FRAC':
      # loop through the coords until we get to the endblock statement and read each line into a list
      stop = 'no'
      coordsList = []
      while stop == 'no':
        i+=1
        words = lines[i].split()
        if str.upper(words[0]) == '%ENDBLOCK':
          stop = 'yes'
          break
        coordsList.append(lines[i])
      i+=1 # skip endblock statement
      # process the list into numpy array
      elements = []
      coords = []
      for line in coordsList:
        words = line.split()
        elements.append(words[0])
        x = float(words[1])
        y = float(words[2])
        z = float(words[3])
        coords.append([x,y,z])
      coords = np.array(coords)
      elements = np.array(elements)
      

    # write line to list
    cellFileList.append(lines[i])
    
    # add one to loop counter
    i+=1

  return unitcell, elements, coords, cellFileList



####################################################################################################
# Writes cell file
####################################################################################################
def writeCellDetailed(name,unitcell,elements,coords,cellFileContents):

  import numpy as np
  # add the .param extension
  filename = name + ".cell"
  
  # Output to screen
  print()
  print("Opening "+ filename +" for writing...")

  # Open file
  myfile = open(filename, "w")

  # write unit cell
  myfile.write('%BLOCK LATTICE_CART\n')
  for vector in unitcell:
    myfile.write('{:20}{:20}{:20}\n'.format(vector[0],vector[1],vector[2]))
  myfile.write('%ENDBLOCK LATTICE_CART\n\n')

  # write coords
  myfile.write('%BLOCK POSITIONS_FRAC\n')
  xyz = np.vstack((elements.T,coords.T)).T
  for line in xyz:
    myfile.write('{:20}{:20}{:20}{:20}\n'.format(line[0],line[1],line[2],line[3]))
  myfile.write('%ENDBLOCK POSITIONS_FRAC\n\n')
  
  for line in cellFileContents:
    myfile.write(line)

  print("DONE")
  print()
    
  # Close file
  myfile.close()
  return



####################################################################################################
# Modify cell list
# Takes as input a list of strings that is the original cell file
# Modifies one part of it, which is specified by the option "param".
####################################################################################################
def modifyCell(cellList,param,value):

  print("Modifying cell file, parameter:",param)
  
  newCellList = []

  # how many lines in the cell list 
  length = len(cellList)

  # if parameter is "vac" meaning we are changing the vacuum (z) separation:
  if param == 'vac':
    i = 0 
    while i < length:
      words = cellList[i].split()
      numwords = len(words)
      if numwords > 0 and str.upper(words[0]) == '%BLOCK' and str.upper(words[1]) == 'LATTICE_CART':
        break
      i+=1

    # The line number of the cellList that contains the z specification (assumes cubic cell)
    cellLine = i+3

    # modify
    line = cellList[cellLine]
    words = line.split()
    newCellList = cellList
    newCellList[cellLine] = "\t"+words[0]+"\t"+words[1]+"\t"+str(float(value))+"\n"

  # THIS FUNCTION CAN BE MODIFIED TO ADD MORE POSSIBLE CHANGES TO A CELL FILE
  # THIS CAN BE DONE BY ADDING HERE A STATEMENT:
  # if param == 'yourparam'
  # FOLLOWED BY SUITABLE CODE FOR SEARCHING AND MODIFYING THE CELL LIST
  
  return newCellList





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
    filenameList = ["Filename"]
    energyList = ["TotalE"]
    cutoffList = ["Cutoff"]
    bondList = ["Bondlength"]
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

            if numwords > 5 and words[0] == 'Si' and words[1] == '1' and words[3] == 'Si':
                bondlength = float(words[6])

            if numwords > 8 and words[0] == '***' and words[6] == 'warnings':
                warnings = int(words[5])

            # This is just output to the screen - show summary of warnings
            # The number of warnings is also written to the output file.
            # These are just checks to make sure we catch any errors.
            #if numwords > 0 and words[0] == 'WARNING':
            if 'WARNING' in line:
                print('WARNING in '+filename+": "+line,end='')
            if 'warning' in line:
                print('WARNING in '+filename+": "+line,end='')
                
        nameNoExt = str(os.path.splitext(filename)[0])
        
        filenameList.append(nameNoExt)
        bondList.append(bondlength)
        energyList.append(finalE)
        cutoffList.append(cutoffE)
        warningsList.append(warnings)
        
        # Close file
        myfile.close()
        
    # convert final lists to numpy arrays
    filenameList = np.array(filenameList)
    cutoffList = np.array(cutoffList)
    energyList = np.array(energyList)
    bondList = np.array(bondList)
    warningsList = np.array(warningsList)

    returnArray = np.transpose([filenameList,cutoffList,energyList,bondList,warningsList])

    return returnArray



####################################################################################################
# Get information from .castep output file
####################################################################################################
def getTotalEnergyConvergence(filename):
    import os
    import numpy as np

    # Just the name, no extension
    name = filename

    # with .castep extension
    castepfile = filename+".castep"
    
    # check the castep file for errors (display them on screen)
    with open(castepfile,'r') as myfile:
        for line in myfile:
            if 'WARNING' in line:
                print('WARNING in '+filename+': '+line,end='')
            if 'warning' in line:
                print('WARNING in '+filename+': '+line,end='')
        
    # with .geom extension - use this file for getting final energies for each step
    filename = name+".geom"

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
