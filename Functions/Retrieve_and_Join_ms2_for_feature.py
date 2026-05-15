from __future__ import annotations

import numpy as np
import os
import pandas as pd

def Retrieve_and_Join_ms2_for_feature(All_FeaturesTable,
                                      Feature_module,
                                      SamplesNames,
                                      sample_id_col = 16,
                                      ms2_spec_id_col = 15,
                                      ms2Folder = 'ms2_spectra',
                                      ToAdd = 'mzML',
                                      Norm2One = False):
    N_features = len(Feature_module)
    FeatureTable = All_FeaturesTable[Feature_module, :].copy()
    firstSpec = True
    All_ms2 = []
    spectra_count = 0
    Spectra_idVec = []
    for feature_id in np.arange(N_features,dtype = 'int'):
        features_stats = FeatureTable[feature_id, :]
        if sample_id_col > 0:
            sample_id = int(features_stats[sample_id_col])
        else:
            sample_id = 0
        ms2_spec_id = str(int(features_stats[ms2_spec_id_col]))
        sample_name_id = SamplesNames[sample_id] + ToAdd
        ms2_spectrumLoc = ms2Folder + '/' + sample_name_id + '/' + ms2_spec_id + '.csv'        
        ExistSpectrum = os.path.exists(ms2_spectrumLoc)
        if ExistSpectrum:                        
            ms2_spectrumDF = pd.read_csv(ms2_spectrumLoc, index_col = 0)
            ms2_spectrum = np.array(ms2_spectrumDF)      
            if Norm2One:
                Norm = np.sqrt(np.sum(ms2_spectrum[:, 9] * ms2_spectrum[:, 9]))
                ms2_spectrum[:, 9] = ms2_spectrum[:, 9] / Norm
            N_peaks = len(ms2_spectrum[:, 0])
            SpectrumLocVec = np.ones(N_peaks).reshape(-1, 1) * spectra_count
            ms2_spectrum = np.append(ms2_spectrum,SpectrumLocVec, axis = 1)
            Spectra_idVec.append(int(feature_id))
            spectra_count += 1
            if firstSpec:
                All_ms2 = ms2_spectrum.copy()
                firstSpec = False
            else:
                All_ms2 = np.append(All_ms2,ms2_spectrum, axis = 0)   
    if len(All_ms2) == 0:
        return [[], []]
    return [All_ms2, Spectra_idVec]