from __future__ import annotations

import numpy as np

def classical_pcoa(distance_matrix,
                   n_components = 2):
    """
    Compute classical principal coordinates analysis from a distance matrix.
    """

    distance_matrix = np.asarray(distance_matrix,
                                 dtype = float)

    n_samples = distance_matrix.shape[0]

    centering_matrix = np.eye(n_samples) - np.ones((n_samples,
                                                    n_samples)) / n_samples

    squared_distance_matrix = distance_matrix ** 2

    gram_matrix = -0.5 * centering_matrix @ squared_distance_matrix @ centering_matrix

    eigenvalues, eigenvectors = np.linalg.eigh(gram_matrix)

    order = np.argsort(eigenvalues)[::-1]

    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    positive_eigenvalues = np.maximum(eigenvalues[:n_components],
                                      0)

    coordinates = eigenvectors[:, :n_components] * np.sqrt(positive_eigenvalues)

    explained_fraction = eigenvalues[:n_components] / np.sum(eigenvalues[eigenvalues > 0])

    return coordinates, explained_fraction, eigenvalues