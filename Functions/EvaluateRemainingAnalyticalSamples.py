from __future__ import annotations
from ContrastSamplesCentroids import *
from FeatureClusterCentroids import *
from FillAlignedFragmentsSamplesSpectraMat import *
from Retrieve_and_Join_ms2_for_feature import *
from SamplingSamplesSpectra import *

def EvaluateRemainingAnalyticalSamples(Samples_FeaturesIdsList,
                                       Samples_ids2Check,
                                       feature_cluster_data,
                                       All_FeaturesTable,
                                       SamplesNames,
                                       BigFeature_Module,
                                       IntramoduleSimilarityModulesMat,
                                       modules_silhouette_summary_table,
                                       sample_id_col = 16,
                                       ms2_spec_id_col = 15,
                                       ms2Folder = 'ms2_spectra',
                                       ToAdd = 'mzML',
                                       Norm2One = False,
                                       Nspectra_sampling = 3,
                                       std_distance = 3,
                                       ppm_tol = 20):

    Modules, Feature_Module, IntramoduleSimilarity, _, AlignedFragmentsMat, AlignedFragments_mz_Mat, modules_silhouette_summary_table = feature_cluster_data
    N_modules = len(Modules)

    ConfirmedModulesPerSample = {sample_id: set() for sample_id in Samples_ids2Check}
    RemainingSpectraPerSample = {sample_id: list(Samples_FeaturesIdsList[sample_id])
                                 for sample_id in Samples_ids2Check}

    CentroidsAlignedFragmentsMat = FeatureClusterCentroids(
                                       feature_cluster_data = feature_cluster_data)

    while len(Samples_ids2Check) > 0:

        # 1. Generate the random sample request
        SamplesSamplesList_requested = SamplingSamplesSpectra(
                                         Samples_FeaturesIdsList = RemainingSpectraPerSample,
                                         Samples_ids2Check = Samples_ids2Check,
                                         Nspectra_sampling = Nspectra_sampling)

        # 2. IMMEDIATELY remove these from the pool so we don't sample them again,
        # even if they fail to load from disk.
        for true_spectrum_id in SamplesSamplesList_requested:
            sample_id = int(All_FeaturesTable[true_spectrum_id, sample_id_col])
            if true_spectrum_id in RemainingSpectraPerSample[sample_id]:
                RemainingSpectraPerSample[sample_id].remove(true_spectrum_id)

        # 3. Try to load them from disk
        All_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = All_FeaturesTable,
                                                                   Feature_module = SamplesSamplesList_requested,
                                                                   SamplesNames = SamplesNames,
                                                                   sample_id_col = sample_id_col,
                                                                   ms2_spec_id_col = ms2_spec_id_col,
                                                                   ms2Folder = ms2Folder,
                                                                   ToAdd = ToAdd,
                                                                   Norm2One = Norm2One)

        # 4. Only process centroids if we actually loaded some spectra
        if len(All_ms2) > 0:
            # Get the list of spectra that actually successfully loaded
            SamplesSamplesList_successful = np.array(SamplesSamplesList_requested)[Spectra_idVec].tolist()

            AlignedFragmentsSamplesSpectraMat, AlignedFragmentsSamplesSpectra_mz_Mat = \
                FillAlignedFragmentsSamplesSpectraMat(
                    AlignedFragmentsMat = AlignedFragmentsMat,
                    AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                    All_ms2 = All_ms2,
                    SamplesSamplesList = SamplesSamplesList_successful,
                    std_distance = std_distance,
                    ppm_tol = ppm_tol)

            CosineToCentroids = ContrastSamplesCentroids(AlignedFragmentsSamplesSpectraMat = AlignedFragmentsSamplesSpectraMat,
                                                         CentroidsAlignedFragmentsMat = CentroidsAlignedFragmentsMat,
                                                         N_modules = N_modules)

            # Match logic
            for spectrum_idx, true_spectrum_id in enumerate(SamplesSamplesList_successful):
                sample_id = int(All_FeaturesTable[true_spectrum_id, sample_id_col])
                
                for module_id in np.arange(N_modules):
                    if module_id in ConfirmedModulesPerSample[sample_id]:
                        continue

                    best_cosine = CosineToCentroids[spectrum_idx, module_id]
                    module_threshold = IntramoduleSimilarityModulesMat[module_id, 1]

                    if best_cosine >= module_threshold:
                        Modules[module_id].append(true_spectrum_id)
                        if true_spectrum_id not in BigFeature_Module:
                            BigFeature_Module.append(true_spectrum_id)
                        ConfirmedModulesPerSample[sample_id].add(module_id)

        # 5. ALWAYS execute this cleanup block, NEVER use 'continue' to skip it!
        Samples_ids_to_remove = []
        for sample_id in Samples_ids2Check:
            AllModulesResolved = len(ConfirmedModulesPerSample[sample_id]) == N_modules
            NoSpectraLeft = len(RemainingSpectraPerSample[sample_id]) == 0
            if AllModulesResolved or NoSpectraLeft:
                Samples_ids_to_remove.append(sample_id)

        for sample_id in Samples_ids_to_remove:
            Samples_ids2Check.remove(sample_id)

    # Note: AlignedFragmentsSamplesSpectraMat might not exist if the loop exited early 
    # due to missing files, so we pass the original matrices back safely.
    feature_cluster_data = [Modules,
                            BigFeature_Module,
                            IntramoduleSimilarityModulesMat,
                            All_FeaturesTable,
                            AlignedFragmentsMat,
                            AlignedFragments_mz_Mat,
                            modules_silhouette_summary_table] 
    
    return feature_cluster_data