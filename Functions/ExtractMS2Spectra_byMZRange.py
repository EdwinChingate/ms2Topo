from pyopenms import *
def ExtractMS2Spectra_byMZRange(DataSet,
                                min_mz=0,
                                max_mz=1e4,
                                min_RT=0,
                                max_RT=1e5):
    """
    Iterates over all spectra in a DataSet (MSExperiment),
    keeps only MS2 spectra whose precursor m/z falls within
    [min_mz, max_mz] and whose RT falls within [min_RT, max_RT].
    Returns a list of qualifying MSSpectrum objects.
    """
    FilteredSpectra = []

    for SpectralSignals in DataSet:
        MSLevel = SpectralSignals.getMSLevel()
        if MSLevel != 2:
            continue

        RT = SpectralSignals.getRT()
        if RT < min_RT or RT > max_RT:
            continue

        Precursor = SpectralSignals.getPrecursors()[0]
        MZ = Precursor.getMZ()
        if MZ < min_mz or MZ > max_mz:
            continue

        FilteredSpectra.append(SpectralSignals)

    return FilteredSpectra
