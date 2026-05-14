from __future__ import annotations
def clustering_spectra_with_spectral_clustering(Feature_module,
                                                All_FeaturesTable,
                                                SamplesNames,
                                                std_times = 1,
                                                Intensity_to_explain = 0.9,
                                                min_spectra_fraction = 0.3,
                                                cos_tol = 0.9,
                                                percentile = 10,
                                                percentile_mz = 5,
                                                percentile_Int = 10,
                                                slice_id = 0,
                                                max_Nspectra_cluster = 8,
                                                Nspectra_sampling = 54,
                                                SamplingTimes = 20,
                                                sample_id_col = 16,
                                                ms2_spec_id_col = 15,
                                                ms2Folder = 'ms2_spectra',
                                                ToAdd = 'mzML',
                                                Norm2One = False):
    """
    Orchestrate MS2 spectral clustering for one raw feature module.

    Flow:
        1. Retrieve and align MS2 spectra.
        2. Estimate k with resampled spectral clustering.
        3. Run the final spectral partition on the full aligned-fragment matrix.
        4. Build feature_cluster_data in the downstream ms2Topo format.
    """
    n_spectra = len(Feature_module)
    min_spectra = int(np.ceil(min_spectra_fraction * n_spectra))
    aligned_fragments_mat, aligned_fragments_mz_mat, explained_fraction_int, n_features, Spectra_idVec = align_fragments_engine(All_FeaturesTable = All_FeaturesTable,

    filtered_feature_module = np.array(Feature_module)[Spectra_idVec].tolist()

    n_spectra = aligned_fragments_mat.shape[1] - 1

    current_sampling_size = min(Nspectra_sampling,
                                n_spectra)

    max_n_clusters = min(max_Nspectra_cluster,
                         current_sampling_size)


    n_clusters, all_modules_by_iteration, sampled_spectra_by_iteration = estimate_k_by_resampled_spectral_clustering(aligned_fragments_mat = aligned_fragments_mat,
                                                                                                                     max_n_clusters = max_n_clusters,
                                                                                                                     n_iterations = SamplingTimes,
                                                                                                                     std_times = std_times,
                                                                                                                     current_sampling_size = current_sampling_size,
                                                                                                                     min_nodes = 1,
                                                                                                                     assign_labels = 'discretize',
                                                                                                                     random_state = 0)

    cosine_matrix = CosineMatrix(AlignedFragmentsMat = aligned_fragments_mat,
                                 N_features = n_spectra)

    if n_clusters == 1:
        modules = np.array([set(range(n_spectra))],
                           dtype = object)
    else:
        modules = sklearn_spectral_modules_from_cosine_matrix(cosine_matrix = cosine_matrix,
                                                              n_clusters = n_clusters,
                                                              min_nodes = 1,
                                                              assign_labels = 'discretize',
                                                              random_state = 0)

    IntramoduleSimilarity = IntramoduleSimilarityCalc(Modules = modules,
                                                      CosineMat = cosine_matrix.copy(),
                                                      percentile = percentile)

    modules_silhouette_summary_table = all_modules_silhouette_vector_summarizer(CosineMat = cosine_matrix,
                                                                                modules = modules,
                                                                                percentile = percentile)

    Modules = [list(module) for module in modules]

    This_Module_FeaturesTable = np.hstack((All_FeaturesTable[filtered_feature_module, :].copy(),
                                           explained_fraction_int.reshape(-1, 1)))

    This_Module_FeaturesTable = np.hstack((This_Module_FeaturesTable,
                                           slice_id * np.ones(len(explained_fraction_int)).reshape(-1, 1)))

    feature_cluster_data = [Modules,
                            filtered_feature_module,
                            IntramoduleSimilarity,
                            This_Module_FeaturesTable,
                            aligned_fragments_mat,
                            aligned_fragments_mz_mat,
                            modules_silhouette_summary_table]

    sampling_samples = current_sampling_size

    return [feature_cluster_data,
            sampling_samples]


# In[13]: