from __future__ import annotations

from ClosingModule import *

def Update_ids_FeatureModules(context,
                              params):
    """
    Update feature IDs from a dictionary-based feature_cluster_data object.

    Expected context keys:
        feature_cluster_data, AlignedSamplesList, SamplesNames, feature_id,
        sampling_samples
    """

    feature_cluster_data = context["feature_cluster_data"]
    AlignedSamplesList = context["AlignedSamplesList"]
    SamplesNames = context["SamplesNames"]
    feature_id = context.get("feature_id", 0)
    sampling_samples = context.get("sampling_samples", 0)

    if len(feature_cluster_data) == 0:
        return [feature_id, AlignedSamplesList]

    Modules = feature_cluster_data["Modules"]
    Feature_module = feature_cluster_data["Feature_module"]
    All_FeaturesTable = feature_cluster_data["All_FeaturesTable"]
    AlignedFragmentsMat = feature_cluster_data["AlignedFragmentsMat"]
    AlignedFragments_mz_Mat = feature_cluster_data["AlignedFragments_mz_Mat"]
    modules_silhouette_summary_table = feature_cluster_data["modules_silhouette_summary_table"]

    module_id = 0

    for module in Modules:
        IntramoduleCosineStatsVec = modules_silhouette_summary_table[module_id, 1: 6]

        closing_context = {
            "module": module,
            "Feature_module": Feature_module,
            "All_FeaturesTable": All_FeaturesTable,
            "AlignedFragmentsMat": AlignedFragmentsMat,
            "AlignedFragments_mz_Mat": AlignedFragments_mz_Mat,
            "AlignedSamplesList": AlignedSamplesList,
            "SamplesNames": SamplesNames,
            "IntramoduleCosineStatsVec": IntramoduleCosineStatsVec,
            "feature_id": feature_id,
            "sampling_samples": sampling_samples,
        }

        feature_id, AlignedSamplesList = ClosingModule(context = closing_context,
                                                       params = params)
        module_id += 1

    return [feature_id, AlignedSamplesList]