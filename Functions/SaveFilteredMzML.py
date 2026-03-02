from pyopenms import *

def SaveFilteredMzML(FilteredDataSet, OutputFolder, OutputFileName):
    """
    Writes the FilteredDataSet (MSExperiment) to an .mzML file
    in the specified OutputFolder.
    Creates the OutputFolder if it does not already exist.
    """
    if not os.path.exists(OutputFolder):
        os.makedirs(OutputFolder)

    OutputPath = OutputFolder + '/' + OutputFileName
    MzMLFile().store(OutputPath, FilteredDataSet)

    return OutputPath
