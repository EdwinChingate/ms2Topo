import numpy as np
def minimalSpectrum(FragmentsVec,
                    FragmentAbundanceVec,
                    fractionIntensity = 0,
                    RareFragmentsList = [],
                    FragmentsList = [],
                    min_spectra = 3,
                    min_fractionIntensity = 0.9):
    FragmentsLeft = list(set(list(range(len(FragmentsVec)))) - set(FragmentsList))
    FractionContributionOrder = (-FragmentsVec[FragmentsLeft]).argsort()
    FractionContributionOrder = [int(fragment) for fragment in FractionContributionOrder]
    FractionContributionOrder = np.array(FragmentsLeft)[FractionContributionOrder].tolist()
    while (fractionIntensity < min_fractionIntensity) and (len(FractionContributionOrder) > 0):
        fragment_id = int(FractionContributionOrder[0])
        if FragmentsVec[fragment_id] == 0:
            break                
        if FragmentAbundanceVec[fragment_id] > min_spectra:
            fractionIntensity += FragmentsVec[fragment_id]
            FragmentsList.append(fragment_id)
        else: 
            RareFragmentsList.append(fragment_id)
        FractionContributionOrder = np.delete(FractionContributionOrder, 0)
    if (fractionIntensity < min_fractionIntensity) and (min_spectra > 0):
        RareFragmentsList, FragmentsList, fractionIntensity = minimalSpectrum(FragmentsVec = FragmentsVec,
                                                                              FragmentAbundanceVec = FragmentAbundanceVec,
                                                                              fractionIntensity = fractionIntensity,
                                                                              RareFragmentsList = RareFragmentsList,
                                                                              FragmentsList = FragmentsList,
                                                                              min_spectra = 0,
                                                                              min_fractionIntensity = min_fractionIntensity)        
    return [RareFragmentsList, FragmentsList, fractionIntensity]
