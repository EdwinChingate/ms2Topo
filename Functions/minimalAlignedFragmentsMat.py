import numpy as np
from minimalSpectrum import *
def minimalAlignedFragmentsMat(AlignedFragmentsMat,
                               Intensity_to_explain = 0.9,
                               min_spectra = 3):    
    BinaryAlignedFragmentsMat = (AlignedFragmentsMat[:,1:] > 0).astype(int)
    FragmentAbundanceVec = np.sum(BinaryAlignedFragmentsMat, axis = 1)
    IntensityContributionVec = np.sum(AlignedFragmentsMat[:,1:], axis = 0)
    N_spectra = BinaryAlignedFragmentsMat.shape[1]
    Fragments_to_consider = []
    for spectrum_id in np.arange(N_spectra):
        FragmentsVec = AlignedFragmentsMat[:,spectrum_id+1]
        RareFragmentsList, FragmentsList, fractionIntensity = minimalSpectrum(FragmentsVec = FragmentsVec,
                                                                              FragmentAbundanceVec = FragmentAbundanceVec,
                                                                              min_spectra = min_spectra,
                                                                              fractionIntensity = 0,
                                                                              RareFragmentsList = [],
                                                                              FragmentsList = [],
                                                                              min_fractionIntensity = Intensity_to_explain*IntensityContributionVec[spectrum_id])
            
        Fragments_to_consider += FragmentsList
    Fragments_to_consider = list(set(Fragments_to_consider))
    return AlignedFragmentsMat[Fragments_to_consider,:]

