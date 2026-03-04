from __future__ import annotations
from ClusteringSamplingModules import *
from ContrastSamplesCentroids import *
from FeatureClusterCentroids import *
from FeaturesTableSamples2Check import *
from FillAlignedFragmentsSamplesSpectraMat import *
from FormattingSummary import *
from MatchSampleSpectra_with_Centroid import *
from ReOrganizeSamplingResults import *
from Retrieve_ms2_afterSampling import *

def SummarizeSampling(feature_clusterList,
                      All_FeaturesTable,
                      SamplesNames,
                      Original_Feature_module,
                      min_spectra = 3,
                      Intensity_to_explain = 0.9,
                      cos_tol = 0.9,
                      percentile = 10,
                      slice_id = 0,
                      sample_id_col = 16,
                      ms2_spec_id_col = 15,
                      percentile_mz = 5,
                      percentile_Int = 10,
                      Nspectra_sampling = 3,      # ← ADDED: needed by Retrieve_ms2_afterSampling
                      ms2Folder = 'ms2_spectra',
                      ToAdd = 'mzML',
                      Norm2One = False):

    All_consensus_ms2, ModulesList, IntramoduleSimilarityList, BigFeature_Module = ReOrganizeSamplingResults(
                             feature_clusterList = feature_clusterList,
                             min_spectra = min_spectra,
                             percentile_mz = percentile_mz,
                             percentile_Int = percentile_Int)

    print(len(feature_clusterList))

    feature_cluster_data, Explained_fractionInt = ClusteringSamplingModules(  # ← FIXED: unpack Explained_fractionInt
                             All_consensus_ms2 = All_consensus_ms2,
                             ModulesList = ModulesList,
                             IntramoduleSimilarityList = IntramoduleSimilarityList,
                             BigFeature_Module = BigFeature_Module,
                             All_FeaturesTable = All_FeaturesTable,
                             SamplesNames = SamplesNames,
                             min_spectra = min_spectra,
                             Intensity_to_explain = Intensity_to_explain,
                             cos_tol = cos_tol,
                             percentile = percentile,
                             slice_id = slice_id,
                             sample_id_col = sample_id_col,
                             ms2_spec_id_col = ms2_spec_id_col,
                             ms2Folder = ms2Folder,
                             ToAdd = ToAdd,
                             Norm2One = Norm2One)

    Modules, Feature_Module, IntramoduleSimilarityModulesMat, _, AlignedFragmentsMat, _ = feature_cluster_data  # ← ADDED: unpack for downstream use
    N_modules = len(Modules)  # ← ADDED: needed by ContrastSamplesCentroids

    Samples_FeaturesIdsList, Samples_ids2Check = FeaturesTableSamples2Check(
                             Feature_Module = BigFeature_Module,
                             Original_Feature_module = Original_Feature_module,
                             All_FeaturesTable = All_FeaturesTable,
                             sample_id_col = sample_id_col)

    print(Samples_ids2Check)

    if len(Samples_ids2Check) == 0:
        feature_cluster_data = FormattingSummary(feature_cluster_data = feature_cluster_data,
                                                 Explained_fractionInt = Explained_fractionInt,
                                                 slice_id = slice_id)
        return feature_cluster_data  # ← FIXED: was returning before FormattingSummary

    SamplesSamplesList, All_ms2 = Retrieve_ms2_afterSampling(
                             Samples_FeaturesIdsList = Samples_FeaturesIdsList,
                             Samples_ids2Check = Samples_ids2Check,
                             All_FeaturesTable = All_FeaturesTable,
                             SamplesNames = SamplesNames,
                             sample_id_col = sample_id_col,
                             ms2_spec_id_col = ms2_spec_id_col,
                             ms2Folder = ms2Folder,
                             ToAdd = ToAdd,
                             Norm2One = Norm2One,
                             Nspectra_sampling = Nspectra_sampling)

    AlignedFragmentsSamplesSpectraMat = FillAlignedFragmentsSamplesSpectraMat(
                             AlignedFragmentsMat = AlignedFragmentsMat,
                             All_ms2 = All_ms2,
                             SamplesSamplesList = SamplesSamplesList)

    CentroidsAlignedFragmentsMat = FeatureClusterCentroids(
                             feature_cluster_data = feature_cluster_data)

    CosineToCentroids = ContrastSamplesCentroids(
                             AlignedFragmentsSamplesSpectraMat = AlignedFragmentsSamplesSpectraMat,
                             CentroidsAlignedFragmentsMat = CentroidsAlignedFragmentsMat,
                             N_modules = N_modules)

    Modules, BigFeature_Module = MatchSampleSpectra_with_Centroid(
                             CosineToCentroids = CosineToCentroids,
                             SamplesSamplesList = SamplesSamplesList,
                             Modules = Modules,
                             BigFeature_Module = BigFeature_Module,
                             IntramoduleSimilarityModulesMat = IntramoduleSimilarityModulesMat)

    # Update feature_cluster_data with expanded Modules and BigFeature_Module
    # before passing to FormattingSummary
    feature_cluster_data = [Modules,
                            BigFeature_Module,
                            IntramoduleSimilarityModulesMat,
                            All_FeaturesTable,
                            AlignedFragmentsMat,
                            feature_cluster_data[5]]  # ← AlignedFragments_mz_Mat preserved

    feature_cluster_data = FormattingSummary(feature_cluster_data = feature_cluster_data,
                                             Explained_fractionInt = Explained_fractionInt,
                                             slice_id = slice_id)
    return feature_cluster_data