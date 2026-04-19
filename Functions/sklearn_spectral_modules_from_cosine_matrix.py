from __future__ import annotations
import numpy as np

# TODO: unresolved names: SpectralClustering

def sklearn_spectral_modules_from_cosine_matrix(cosine_matrix,
                                                n_clusters,
                                                min_nodes = 3,
                                                assign_labels = 'discretize',
                                                random_state = 0,
                                                clip_negative = True,
                                                unit_diagonal = True):

    affinity_matrix = np.array(cosine_matrix,
                               dtype = float).copy()

    affinity_matrix = (affinity_matrix + affinity_matrix.T) / 2

    if clip_negative:
        affinity_matrix[affinity_matrix < 0] = 0

    if unit_diagonal:
        np.fill_diagonal(affinity_matrix,
                         1)

    spectral_model = SpectralClustering(n_clusters = n_clusters,
                                        affinity = 'precomputed',
                                        assign_labels = assign_labels,
                                        random_state = random_state)

    labels = spectral_model.fit_predict(affinity_matrix)

    modules = []

    for module_id in range(n_clusters):
        module = set(np.where(labels == module_id)[0].astype(int).tolist())

        if len(module) >= min_nodes:
            modules.append(module)

    return np.array(modules,
                    dtype = object)


# In[172]: