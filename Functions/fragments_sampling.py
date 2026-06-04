from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from show_df import *
from adjacent_neutral_losses import *

def fragments_sampling(mz_vec,
                       current_sampling_size):

    rng = np.random.default_rng()
    n_fragments = mz_vec.shape[0]


    sampled_fragment_ids = rng.choice(np.arange(n_fragments),
                                      size = current_sampling_size,
                                      replace = False).tolist()
    print( mz_vec[sampled_fragment_ids])

    neutral_losses_adjacency_matrix = adjacent_neutral_losses(neutral_losses_array = mz_vec[sampled_fragment_ids],
                                                              mz_tol = 1e-4)
    show_df(neutral_losses_adjacency_matrix)
    G = nx.from_numpy_array(neutral_losses_adjacency_matrix)


    nx.draw(G, with_labels=True, node_color="lightblue", font_weight="bold")
    plt.show()
