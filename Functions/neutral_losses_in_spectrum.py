from __future__ import annotations

import numpy as np

def neutral_losses_in_spectrum(fragments_array,
                               min_neutral_loss = 18):

    n_fragments = len(fragments_array)
    #a list would work better than a matrix
    neutral_losses_fragments_matrix = np.zeros((n_fragments, n_fragments))

    for fragment_id_1 in range(n_fragments):
        for fragment_id_2 in range(fragment_id_1 + 1, n_fragments):
            neutral_loss = fragments_array[fragment_id_2] - fragments_array[fragment_id_1]
            if neutral_loss < min_neutral_loss:
                continue
            neutral_losses_fragments_matrix[fragment_id_1, fragment_id_2] = neutral_loss

    neutral_losses_fragments_vector = neutral_losses_fragments_matrix.flatten()
    return neutral_losses_fragments_vector[neutral_losses_fragments_vector > 0].tolist()
