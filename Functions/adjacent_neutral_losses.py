from __future__ import annotations

import numpy as np

def adjacent_neutral_losses(neutral_losses_array,
                            mz_tol = 2e-4):

    n_fragments = len(neutral_losses_array)
    neutral_losses_adjacency_matrix = np.zeros((n_fragments, n_fragments))

    for neutral_loss_id_1 in range(n_fragments):
        for neutral_loss_id_2 in range(neutral_loss_id_1 + 1, n_fragments):
            mz_difference = np.abs(neutral_losses_array[neutral_loss_id_2] - neutral_losses_array[neutral_loss_id_1])
            if mz_difference > mz_tol:
                continue
            neutral_losses_adjacency_matrix[neutral_loss_id_1, neutral_loss_id_2] = mz_difference
            neutral_losses_adjacency_matrix[neutral_loss_id_2, neutral_loss_id_1] = mz_difference

    return neutral_losses_adjacency_matrix
