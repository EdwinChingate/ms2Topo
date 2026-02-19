

import numpy as np
from minimalSpectrum import *
def minimalAlignedFragmentsMat(AlignedFragmentsMat,
                               AlignedFragments_mz_Mat,
                               Intensity_to_explain = 0.9,
                               min_spectra = 3):    
    BinaryAlignedFragmentsMat = (AlignedFragmentsMat[:,1:] > 0).astype(int)
    FragmentAbundanceVec = np.sum(BinaryAlignedFragmentsMat, axis = 1)
    IntensityContributionVec = np.sum(AlignedFragmentsMat[:,1:], axis = 0)
    N_spectra = BinaryAlignedFragmentsMat.shape[1]
    Explained_fractionInt = np.zeros(N_spectra)    
    Fragments_to_consider = []
    for spectrum_id in np.arange(N_spectra):
        FragmentsVec = AlignedFragmentsMat[:, spectrum_id+1]
        RareFragmentsList, FragmentsList, fractionIntensity = minimalSpectrum(FragmentsVec = FragmentsVec,
                                                                              FragmentAbundanceVec = FragmentAbundanceVec,
                                                                              min_spectra = min_spectra,
                                                                              fractionIntensity = 0,
                                                                              RareFragmentsList = [],
                                                                              FragmentsList = [],
                                                                              min_fractionIntensity = Intensity_to_explain*IntensityContributionVec[spectrum_id])        
        Fragments_to_consider += FragmentsList
    Fragments_to_consider = list(set(Fragments_to_consider))
    Fragments_to_consider.sort()
    Explained_fractionInt = np.sum(AlignedFragmentsMat[Fragments_to_consider,1:], axis = 0) / IntensityContributionVec
    Explained_fractionInt = Explained_fractionInt.reshape(-1, 1)    
    return [AlignedFragmentsMat[Fragments_to_consider, :], AlignedFragments_mz_Mat[Fragments_to_consider, :], Explained_fractionInt]
