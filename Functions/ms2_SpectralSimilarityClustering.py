from __future__ import annotations

import numpy as np
import pandas as pd
from AdjacencyListFeatures import *
from ms2_FeaturesDifferences import *
from ms2_feat_modules import *

def ms2_SpectralSimilarityClustering(context,
                                     params):
    """
    Cluster all raw feature modules within one m/z slice.

    Expected context keys:
        SummMS2_raw, SamplesNames, slice_id, feature_id
    Optional context key:
        SampleName
    """

    SummMS2_raw = context["SummMS2_raw"]
    SamplesNames = context.get("SamplesNames", [])
    SampleName = context.get("SampleName", "")
    slice_id = context.get("slice_id", 0)
    feature_id = context.get("feature_id", 0)

    if len(SamplesNames) == 0:
        SamplesNames = [SampleName]

    AdjacencyList, feat_ids = AdjacencyListFeatures(MS2_features = SummMS2_raw,
                                                    mz_col = params["columns"]["mz_col"],
                                                    RT_col = params["columns"]["RT_col"],
                                                    RT_tol = params["feature_grouping"]["RT_tol"],
                                                    mz_Tol = params["feature_grouping"]["mz_Tol"])

    RawModules = ms2_feat_modules(AdjacencyList = AdjacencyList,
                                  ms2_ids = feat_ids)

    AlignedSamplesList = []
    N_raw_modules = len(RawModules)

    for feature_module_id in np.arange(N_raw_modules):
        Feature_module = RawModules[feature_module_id]

        feature_context = {
            "All_FeaturesTable": SummMS2_raw,
            "Feature_module": Feature_module,
            "AlignedSamplesList": AlignedSamplesList,
            "SamplesNames": SamplesNames,
            "feature_id": feature_id,
            "slice_id": slice_id,
        }

        feature_id, AlignedSamplesList = ms2_FeaturesDifferences(context = feature_context,
                                                                 params = params)

    feature_descriptor_columns = ['median_mz(Da)',
                                  'min_mz',
                                  'max_mz',
                                  'IQR_mz(ppm)',
                                  'SamplingSamples',
                                  'N_samples',
                                  'N_ms2-spectra',
                                  'min_silhouette',
                                  'Q1_silhouette',
                                  'median_silhouette',
                                  'Q3_silhouette',
                                  'max_silhouette',
                                  'median_RT(s)',
                                  'Q1_RT(s)',
                                  'Q3_RT(s)',
                                  'min_RT(s)',
                                  'max_RT(s)',
                                  'feat_id']

    all_columns = feature_descriptor_columns + SamplesNames

    AlignedSamplesDF = pd.DataFrame(AlignedSamplesList,
                                    columns = all_columns)

    return_columns = np.array(feature_descriptor_columns)[[0, 3, 13, 12, 14, 5, 6, 8, 9, 10, 7, 11, 1, 2, 15, 16, 17]].tolist() + SamplesNames

    return [AlignedSamplesDF[np.array(return_columns)],
            feature_id]