from __future__ import annotations

from ConsensusSpectra import *
from FeatureModuleStats import *
from Write_ms2ids_and_Consensus_ms2Spectra import *

def ClosingModule(context,
                  params):
    """
    Close one final module into consensus spectra and aligned-sample summary.

    Expected context keys:
        module, AlignedFragments_mz_Mat, AlignedFragmentsMat, Feature_module,
        feature_id, All_FeaturesTable, AlignedSamplesList, SamplesNames,
        SilhouetteStatsVec, IntramoduleCosineStatsVec, sampling_samples
    """

    module = context["module"]
    AlignedFragments_mz_Mat = context["AlignedFragments_mz_Mat"]
    AlignedFragmentsMat = context["AlignedFragmentsMat"]
    feature_id = context["feature_id"]
    All_FeaturesTable = context["All_FeaturesTable"]
    AlignedSamplesList = context["AlignedSamplesList"]
    SamplesNames = context["SamplesNames"]
    SilhouetteStatsVec = context["SilhouetteStatsVec"]
    IntramoduleCosineStatsVec = context["IntramoduleCosineStatsVec"]
    sampling_samples = context.get("sampling_samples", 0)

    sample_id_col = params["columns"]["sample_id_col"]
    ms2_spec_id_col = params["columns"]["ms2_spec_id_col"]
    percentile_mz = params["summary"]["percentile_mz"]
    percentile_Int = params["summary"]["percentile_Int"]
    min_spectra = params["closing"]["min_spectra"]
    minSpectra = params["closing"].get("minSpectra", min_spectra)
    alpha = params["closing"].get("alpha", 0.01)

    if len(module) < min_spectra:
        return [feature_id, AlignedSamplesList]

    consensus_spectraDF = ConsensusSpectra(module = module,
                                           min_spectra = min_spectra,
                                           AlignedFragmentsMat = AlignedFragmentsMat,
                                           AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                                           percentile_mz = percentile_mz,
                                           percentile_Int = percentile_Int,
                                           minSpectra = minSpectra,
                                           alpha = alpha)

    if len(consensus_spectraDF) == 0:
        return [feature_id, AlignedSamplesList]

    Write_ms2ids_and_Consensus_ms2Spectra(feature_id = feature_id,
                                          feature_module = module,
                                          consensus_spectraDF = consensus_spectraDF,
                                          All_FeaturesTable = All_FeaturesTable,
                                          sample_id_col = sample_id_col,
                                          ms2_spec_id_col = ms2_spec_id_col,
                                          explained_Int_col = All_FeaturesTable.shape[1] - 2,
                                          summ_ms2_table_id_col = All_FeaturesTable.shape[1] - 3,
                                          module_id_col = All_FeaturesTable.shape[1] - 1)

    AlignedSamplesVec = FeatureModuleStats(All_FeaturesTable = All_FeaturesTable,
                                           module = module,
                                           SamplesNames = SamplesNames,
                                           SilhouetteStatsVec = SilhouetteStatsVec,
                                           IntramoduleCosineStatsVec = IntramoduleCosineStatsVec,
                                           feature_id = feature_id,
                                           sampling_samples = sampling_samples)

    AlignedSamplesList.append(AlignedSamplesVec)
    feature_id += 1

    return [feature_id, AlignedSamplesList]