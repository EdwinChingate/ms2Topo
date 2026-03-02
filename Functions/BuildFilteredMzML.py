from pyopenms import *

def BuildFilteredMzML(DataSet, FilteredSpectra):
    """
    Creates a new MSExperiment containing only the FilteredSpectra.
    Each spectrum carries its own full metadata (precursors, native ID,
    scan info, etc.). Top-level experiment metadata is copied where possible.
    """
    FilteredDataSet = MSExperiment()

    # Attempt to copy top-level metadata via the most common methods
    for method_name in ['getInstrument', 'getSample', 'getContacts',
                        'getSourceFiles', 'getDataProcessing']:
        try:
            getter = getattr(DataSet, method_name)
            setter_name = 's' + method_name[1:]  # getX -> setX
            setter = getattr(FilteredDataSet, setter_name)
            setter(getter())
        except AttributeError:
            pass

    # Add the filtered spectra
    for SpectralSignals in FilteredSpectra:
        FilteredDataSet.addSpectrum(SpectralSignals)

    return FilteredDataSet
