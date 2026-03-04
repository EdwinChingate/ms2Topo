from __future__ import annotations
import numpy as np
from Retrieve_and_Join_ms2_for_feature import *
from SamplingSamplesSpectra import *

def Retrieve_ms2_afterSampling(Samples_FeaturesIdsList,
                               Samples_ids2Check,
                               All_FeaturesTable,
                               SamplesNames,             # ← ADDED: needed by Retrieve_and_Join
                               sample_id_col = 16,       # ← ADDED: needed by Retrieve_and_Join
                               ms2_spec_id_col = 15,     # ← ADDED: needed by Retrieve_and_Join
                               ms2Folder = 'ms2_spectra',# ← ADDED: needed by Retrieve_and_Join
                               ToAdd = 'mzML',           # ← ADDED: needed by Retrieve_and_Join
                               Norm2One = False,         # ← ADDED: needed by Retrieve_and_Join
                               Nspectra_sampling = 3):   # ← MOVED TO END: has default value

    SamplesSamplesList = SamplingSamplesSpectra(
                             Samples_FeaturesIdsList = Samples_FeaturesIdsList,
                             Samples_ids2Check = Samples_ids2Check,
                             Nspectra_sampling = Nspectra_sampling)

    print(SamplesSamplesList)

    All_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(
                                 All_FeaturesTable = All_FeaturesTable,
                                 Feature_module = SamplesSamplesList,
                                 SamplesNames = SamplesNames,
                                 sample_id_col = sample_id_col,
                                 ms2_spec_id_col = ms2_spec_id_col,
                                 ms2Folder = ms2Folder,
                                 ToAdd = ToAdd,
                                 Norm2One = Norm2One)

    SamplesSamplesList = np.array(SamplesSamplesList)[Spectra_idVec].tolist()
    return [SamplesSamplesList, All_ms2]
