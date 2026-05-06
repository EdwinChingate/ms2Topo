from __future__ import annotations
from AlignFragmentsEngine import *
from Retrieve_and_Join_ms2_for_feature import *
from retrieve_ms2_for_clustering import *

# TODO: unresolved names: SamplesNames, all_features_table, ms2Folder, ms2_spec_id_col_g, raw_feature_module, sample_id_col_g

def align_fragments_engine():

    retrieve_ms2_for_clustering()
    all_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = all_features_table,
                                                               Feature_module = raw_feature_module,
                                                               SamplesNames = SamplesNames,
                                                               sample_id_col = sample_id_col_g,
                                                               ms2_spec_id_col = ms2_spec_id_col_g,
                                                               ms2Folder = ms2Folder,
                                                               ToAdd = 'mzML',
                                                               Norm2One = True)
    aligned_fragments_mat, aligned_fragments_mz_mat, explained_fraction_int, n_features = AlignFragmentsEngine(all_ms2 = all_ms2,
                                                                                                                Feature_module = raw_feature_module,
                                                                                                                Intensity_to_explain = 0.9,
                                                                                                                min_spectra = 5)

    return [aligned_fragments_mat, aligned_fragments_mz_mat, explained_fraction_int, n_features]