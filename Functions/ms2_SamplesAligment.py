from __future__ import annotations

import pandas as pd
from ms2_SpectralSimilarityClustering import *

def ms2_SamplesAligment(context,
                        params):
    """
    Run MS2 spectral-similarity clustering across all m/z slices.

    Expected context keys:
        ProjectName, all_summ_ms2_table, EdgesMat, SamplesNames
    Optional context key:
        feature_id
    """

    ProjectName = context["ProjectName"]
    all_summ_ms2_table = context["All_SummMS2Table"]
    edges_matrix = context["EdgesMat"]
    SamplesNames = context["SamplesNames"]
    feature_id = context.get("feature_id", 0)

    aligned_samples_dfs = []

    for low_id_mz, high_id_mz, slice_id in edges_matrix:
        summ_ms2_raw = all_summ_ms2_table[low_id_mz: high_id_mz, :]

        slice_context = {"SummMS2_raw": summ_ms2_raw,
                         "SamplesNames": SamplesNames,
                         "feature_id": feature_id,
                         "slice_id": slice_id}

        AlignedSamplesDF, feature_id = ms2_SpectralSimilarityClustering(context = slice_context,
                                                                        params = params)

        TableLoc = ProjectName + '-' + str(slice_id) + '.csv'
        AlignedSamplesDF.to_csv(TableLoc)

        aligned_samples_dfs.append(AlignedSamplesDF)

    if len(aligned_samples_dfs) == 0:
        return pd.DataFrame()

    return pd.concat(aligned_samples_dfs,
                     ignore_index = True)
