from __future__ import annotations
import numpy as np

def align_ms2_spectra_with_centroids(all_ms2,
                                     reference_fragments_mz_matrix,
                                     std_distance = 3,
                                     ppm_tol = 20):

    reference_mz_vec = reference_fragments_mz_matrix[:, 0]
    n_reference_fragments = len(reference_mz_vec)
    n_spectra = int(np.max(all_ms2[:, 10])) + 1

    aligned_spectra_mat = np.zeros((n_reference_fragments,
                                    n_spectra + 1))
    aligned_spectra_mz_mat = np.zeros((n_reference_fragments,
                                       n_spectra + 1))

    aligned_spectra_mat[:, 0] = reference_mz_vec
    aligned_spectra_mz_mat[:, 0] = reference_mz_vec

    mz_vec = all_ms2[:, 0]
    mz_std_vec = all_ms2[:, 1]
    mz_std_edge_vec = np.minimum(mz_std_vec * std_distance,
                                 ppm_tol / 1e6 * mz_vec)

    mz_max_vec = mz_vec + mz_std_edge_vec
    mz_min_vec = mz_vec - mz_std_edge_vec

    for reference_fragment_id, reference_mz in enumerate(reference_mz_vec):
        mz_loc = np.where((mz_min_vec < reference_mz) &
                          (mz_max_vec > reference_mz))[0]

        for loc in mz_loc:
            spectrum_id = int(all_ms2[loc, 10])
            intensity = all_ms2[loc, 9]
            mz_value = all_ms2[loc, 0]

            if intensity > aligned_spectra_mat[reference_fragment_id, spectrum_id + 1]:
                aligned_spectra_mat[reference_fragment_id, spectrum_id + 1] = intensity
                aligned_spectra_mz_mat[reference_fragment_id, spectrum_id + 1] = mz_value

    return [aligned_spectra_mat,
            aligned_spectra_mz_mat]