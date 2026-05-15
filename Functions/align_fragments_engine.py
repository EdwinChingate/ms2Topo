from __future__ import annotations

from AlignFragmentsEngine import AlignFragmentsEngine
from Retrieve_and_Join_ms2_for_feature import Retrieve_and_Join_ms2_for_feature

def align_fragments_engine(All_FeaturesTable,
                           Feature_module,
                           SamplesNames,
                           sample_id_col,
                           ms2_spec_id_col,
                           ms2Folder = 'ms2_spectra',
                           ToAdd = 'mzML',
                           Norm2One = False,
                           Intensity_to_explain = 0.9,
                           min_spectra = 3):
    """
    Retrieve MS2 spectra for a raw feature module and align their fragments.
    """

    all_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = All_FeaturesTable,
                                                               Feature_module = Feature_module,
                                                               SamplesNames = SamplesNames,
                                                               sample_id_col = sample_id_col,
                                                               ms2_spec_id_col = ms2_spec_id_col,
                                                               ms2Folder = ms2Folder,
                                                               ToAdd = ToAdd,
                                                               Norm2One = Norm2One)

    aligned_fragments_mat, aligned_fragments_mz_mat, explained_fraction_int, n_features = AlignFragmentsEngine(all_ms2 = all_ms2,
                                                                                                               Feature_module = Feature_module,
                                                                                                               Intensity_to_explain = Intensity_to_explain,
                                                                                                               min_spectra = min_spectra)

    return [aligned_fragments_mat,
            aligned_fragments_mz_mat,
            explained_fraction_int,
            n_features,
            Spectra_idVec]