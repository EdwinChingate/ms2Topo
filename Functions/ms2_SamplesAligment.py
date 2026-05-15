from __future__ import annotations

import pandas as pd
from ms2_SpectralSimilarityClustering import *

def ms2_SamplesAligment(context,
                        params):
    """
    Run MS2 spectral-similarity clustering across all m/z slices.

    Expected context keys:
        ProjectName, All_SummMS2Table, EdgesMat, SamplesNames
    Optional context key:
        feature_id
    """

    ProjectName = context["ProjectName"]
    All_SummMS2Table = context["All_SummMS2Table"]
    EdgesMat = context["EdgesMat"]
    SamplesNames = context["SamplesNames"]
    feature_id = context.get("feature_id", 0)

    aligned_samples_dfs = []

    for Low_id_mz, High_id_mz, slice_id in EdgesMat:
        SummMS2_raw = All_SummMS2Table[Low_id_mz: High_id_mz, :]

        slice_context = {"SummMS2_raw": SummMS2_raw,
                         "SamplesNames": SamplesNames,
                         "feature_id": feature_id,
                         "slice_id": slice_id}

        AlignedSamplesDF, feature_id = ms2_SpectralSimilarityClustering(context = slice_context,
                                                                        params = params)

        TableLoc = ProjectName + '-' + str(slice_id) + '.csv'
        # AlignedSamplesDF.to_csv(TableLoc)

        aligned_samples_dfs.append(AlignedSamplesDF)

    if len(aligned_samples_dfs) == 0:
        return pd.DataFrame()

    return pd.concat(aligned_samples_dfs,
                     ignore_index = True)