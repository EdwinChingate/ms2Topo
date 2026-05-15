from __future__ import annotations

from Update_ids_FeatureModules import *
from clustering_spectra_with_spectral_clustering import *

def ms2_FeaturesDifferences(context,
                            params):
    """
    Run spectral clustering for one feature module and update aligned samples.

    Expected context keys:
        All_FeaturesTable, Feature_module, SamplesNames, AlignedSamplesList,
        slice_id, feature_id
    """

    feature_cluster_data, sampling_samples = clustering_spectra_with_spectral_clustering(context = context,
                                                                                         params = params)

    update_context = {
        "feature_cluster_data": feature_cluster_data,
        "AlignedSamplesList": context["AlignedSamplesList"],
        "SamplesNames": context["SamplesNames"],
        "feature_id": context.get("feature_id", 0),
        "sampling_samples": sampling_samples,
    }

    feature_id, AlignedSamplesList = Update_ids_FeatureModules(context = update_context,
                                                               params = params)

    return [feature_id, AlignedSamplesList]