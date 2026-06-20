from __future__ import annotations

import numpy as np
import pandas as pd
from BinomialMixtureModel import *

def fit_bmm_grid(counts,
                 trials,
                 group_idx,
                 k_values = range(2, 41),
                 n_init = 20,
                 random_state = 7):
    """
    Fit several BMMs and keep the best initialization per K.
    """

    results = []
    rng = np.random.default_rng(random_state)

    for k in k_values:
        best_model = None

        for _ in range(n_init):
            seed = int(rng.integers(0, 1_000_000))

            model = BinomialMixtureModel(
                n_clusters=k,
                random_state=seed
            ).fit(
                counts=counts,
                trials=trials,
                group_idx=group_idx
            )

            if best_model is None or model.loglik_ > best_model.loglik_:
                best_model = model

        labels = best_model.labels_
        cluster_sizes = pd.Series(labels).value_counts()

        results.append({
            "k": k,
            "bic": best_model.bic_,
            "aic": best_model.aic_,
            "loglik": best_model.loglik_,
            "n_iter": best_model.n_iter_,
            "min_cluster_size": cluster_sizes.min(),
            "max_cluster_size": cluster_sizes.max(),
            "model": best_model
        })

    return pd.DataFrame(results)
