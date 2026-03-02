from ChargeDataSet_in_AnotherFolder import *
from BuildFilteredMzML import *
from ExtractMS2Spectra_byMZRange import *
from SaveFilteredMzML import *
from pyopenms import *

def ExtractAndSaveMS2_byMZRange(DataSetName,
                                 DataFolder,
                                 OutputFolder,
                                 OutputFileName,
                                 min_mz=0,
                                 max_mz=1e4,
                                 min_RT=0,
                                 max_RT=1e5):
    """
    Full pipeline: loads an .mzML file, extracts MS2 spectra within
    the specified precursor m/z and RT ranges, builds a new MSExperiment
    with all original metadata, and saves it as a new .mzML file.

    Returns the number of MS2 spectra in the filtered file and the
    output file path.
    """
    # Step 1: Load the original dataset
    DataSet = ChargeDataSet_in_AnotherFolder(
        DataSetName=DataSetName,
        DataFolder=DataFolder
    )

    # Step 2: Filter MS2 spectra by precursor m/z (and optionally RT)
    FilteredSpectra = ExtractMS2Spectra_byMZRange(
        DataSet=DataSet,
        min_mz=min_mz,
        max_mz=max_mz,
        min_RT=min_RT,
        max_RT=max_RT
    )

    # Step 3: Build new MSExperiment with original metadata
    FilteredDataSet = BuildFilteredMzML(
        DataSet=DataSet,
        FilteredSpectra=FilteredSpectra
    )

    # Step 4: Save to disk
    OutputPath = SaveFilteredMzML(
        FilteredDataSet=FilteredDataSet,
        OutputFolder=OutputFolder,
        OutputFileName=OutputFileName
    )

    NumFilteredSpectra = len(FilteredSpectra)
    print(f"Extracted {NumFilteredSpectra} MS2 spectra "
          f"(precursor m/z: [{min_mz}, {max_mz}], "
          f"RT: [{min_RT}, {max_RT}])")
    print(f"Saved to: {OutputPath}")

    return NumFilteredSpectra, OutputPath
