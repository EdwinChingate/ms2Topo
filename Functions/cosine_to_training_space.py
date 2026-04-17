from __future__ import annotations
from Cosine_2VecSpec import *
import numpy as np

def cosine_to_training_space(aligned_query_mat,
                             training_mat):

    n_queries = aligned_query_mat.shape[1] - 1
    n_training = training_mat.shape[1] - 1

    cosine_to_training = np.zeros((n_queries,
                                   n_training))

    for query_id in range(n_queries):
        query_vec = aligned_query_mat[:, query_id + 1]

        for train_id in range(n_training):
            train_vec = training_mat[:, train_id + 1]

            aligned_spec_mat = np.column_stack([training_mat[:, 0],
                                                train_vec,
                                                query_vec])

            cosine_to_training[query_id, train_id] = Cosine_2VecSpec(AlignedSpecMat = aligned_spec_mat)

    return cosine_to_training


# In[241]: