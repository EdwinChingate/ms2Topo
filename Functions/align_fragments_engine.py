from __future__ import annotations

from AlignFragmentsEngine import *
from Retrieve_and_Join_ms2_for_feature import *

def align_fragments_engine(context,
                           params):
    """
    Retrieve MS2 spectra for a raw feature module and align their fragments.

    Expected context keys:
        All_FeaturesTable, Feature_module, SamplesNames, min_spectra
    """

    all_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(context = context,
                                                               params = params)

    aligned_fragments_mat, aligned_fragments_mz_mat, explained_fraction_int, n_features = AlignFragmentsEngine(all_ms2 = all_ms2,
                                                                                                               Feature_module = context["Feature_module"],
                                                                                                               Intensity_to_explain = params["alignment"]["Intensity_to_explain"],
                                                                                                               min_spectra = context.get("min_spectra", params["closing"]["min_spectra"]))

    return [aligned_fragments_mat,
            aligned_fragments_mz_mat,
            explained_fraction_int,
            n_features,
            Spectra_idVec]