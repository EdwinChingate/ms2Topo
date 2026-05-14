from __future__ import annotations
import numpy as np
import os
import pandas as pd

# TODO: unresolved names: Spectra_idVec, feature_id, spectra_count

def retrieve_ms2_for_clustering(all_features_table,
                                feature_module,
                                SamplesNames,
                                intensity_to_explain = 0.9,
                                sample_id_col = 16,
                                ms2_spec_id_col = 15,
                                ms2Folder = 'ms2_spectra',
                                ToAdd = 'mzML',
                                Norm2One = False):

    feature_table = all_features_table[feature_module, :]
    features_stats = feature_table[feature_id, :]

    if sample_id_col > 0:
        sample_id = int(features_stats[sample_id_col])
    else:
        sample_id = 0           


    ms2_spec_id = str(int(features_stats[ms2_spec_id_col]))
    sample_name_id = SamplesNames[sample_id] + ToAdd
    ms2_spectrumLoc = ms2Folder + '/' + sample_name_id + '/' + ms2_spec_id + '.csv'
    ExistSpectrum = os.path.exists(ms2_spectrumLoc)

    if not ExistSpectrum:  
        return 

    ms2_spectrumDF = pd.read_csv(ms2_spectrumLoc, index_col = 0)
    ms2_spectrum = np.array(ms2_spectrumDF)     
    norm_sum_intensity_vector = ms2_spectrum[:, 9] / np.sum(ms2_spectrum[:, 9])

    intensity_to_explain

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