from __future__ import annotations
import numpy as np
import pandas as pd

def borda_score_from_silhouette_matrix(silhouette_evaluation_matrix,
                                       k_values,
                                       tie_tol = 1e-2):

    n_iterations, n_k = silhouette_evaluation_matrix.shape
    borda_matrix = np.zeros((n_iterations,
                             n_k))

    for iteration in range(n_iterations):
        silhouette_vector = silhouette_evaluation_matrix[iteration, :]
        valid_loc = np.where(np.isfinite(silhouette_vector))[0]

        if len(valid_loc) == 0:
            continue

        valid_scores = silhouette_vector[valid_loc]
        order = np.argsort(-valid_scores)
        ordered_loc = valid_loc[order]
        ordered_scores = valid_scores[order]

        borda_points = np.arange(len(ordered_scores),
                                 0,
                                 -1,
                                 dtype = float)

        score_id = 0
        while score_id < len(ordered_scores):
            tie_group = [score_id]
            next_score_id = score_id + 1

            while next_score_id < len(ordered_scores):
                if abs(ordered_scores[next_score_id] - ordered_scores[score_id]) <= tie_tol:
                    tie_group.append(next_score_id)
                    next_score_id += 1
                else:
                    break

            mean_borda_points = np.mean(borda_points[tie_group])
            tied_loc = ordered_loc[tie_group]
            borda_matrix[iteration, tied_loc] = mean_borda_points

            score_id = next_score_id

    total_borda_score = np.sum(borda_matrix,
                               axis = 0)
    mean_borda_score = np.mean(borda_matrix,
                               axis = 0)
    win_counts = np.sum(borda_matrix == np.max(borda_matrix,
                                               axis = 1,
                                               keepdims = True),
                        axis = 0)

    borda_summary_df = pd.DataFrame({'k': k_values,
                                     'total_borda_score': total_borda_score,
                                     'mean_borda_score': mean_borda_score,
                                     'win_counts': win_counts})

    borda_summary_df = borda_summary_df.sort_values(by = ['total_borda_score',
                                                          'win_counts',
                                                          'k'],
                                                    ascending = [False,
                                                                 False,
                                                                 True]).reset_index(drop = True)

    return [borda_matrix,
            borda_summary_df]


# In[240]: