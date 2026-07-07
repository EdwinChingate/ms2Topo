# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture


def score_neutral_loss_gmm_components(mz_vec,
                                      min_components = 1,
                                      max_components = 100,
                                      covariance_type = "full",
                                      reg_covar = 1e-12,
                                      max_iter = 1000,
                                      random_state = 7):
    """
    Fit candidate GMMs and return only BIC/AIC scores.

    This is lighter than search_neutral_loss_gmm_components because it does not
    store every fitted model in a dictionary. It is intended for repeated
    resampling iterations.
    """

    mz_vec = np.asarray(mz_vec,
                        dtype = float)

    mz_vec = mz_vec[np.isfinite(mz_vec)]

    if len(mz_vec) == 0:
        raise ValueError("mz_vec has no finite values.")

    min_components = max(int(min_components),
                         1)

    max_components = min(int(max_components),
                         len(mz_vec))

    max_components = max(max_components,
                         min_components)

    X = mz_vec.reshape(-1, 1)

    rows = []

    for n_components in range(min_components,
                              max_components + 1):

        gmm = GaussianMixture(n_components = n_components,
                              covariance_type = covariance_type,
                              reg_covar = reg_covar,
                              max_iter = max_iter,
                              random_state = random_state)

        gmm.fit(X)

        rows.append({"n_components": int(n_components),
                     "BIC": float(gmm.bic(X)),
                     "AIC": float(gmm.aic(X)),
                     "converged": bool(gmm.converged_),
                     "n_iter": int(gmm.n_iter_)})

    score_df = pd.DataFrame(rows)

    selected_n_components = int(score_df.loc[score_df["BIC"].idxmin(),
                                             "n_components"])

    return score_df, selected_n_components
