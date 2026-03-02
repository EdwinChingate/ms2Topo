from pyopenms import *

def ExtractMS2PrecursorMetadata(DataSet):
    """
    Iterates over all spectra in a DataSet and extracts
    precursor m/z and RT for every MS2 spectrum.
    Returns a NumPy array with columns [MZ, RT].
    """
    PrecursorData = []

    for SpectralSignals in DataSet:
        MSLevel = SpectralSignals.getMSLevel()
        if MSLevel != 2:
            continue

        RT = SpectralSignals.getRT()
        Precursor = SpectralSignals.getPrecursors()[0]
        MZ = Precursor.getMZ()

        PrecursorData.append([MZ, RT])

    PrecursorData = np.array(PrecursorData)
    return PrecursorData
