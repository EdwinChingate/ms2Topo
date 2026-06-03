from __future__ import annotations

import numpy as np
from sklearn.mixture import GaussianMixture

def fit_neutral_loss_gmm(mz_vec,
                         n_components,
                         covariance_type="full",
                         reg_covar=1e-12,
                         max_iter=1000,
                         random_state=7):
    """
    Fit a Gaussian mixture model to raw neutral-loss mz observations.
    """

    mz_vec = np.asarray(mz_vec, dtype=float)
    mz_vec = mz_vec[np.isfinite(mz_vec)]

    X = mz_vec.reshape(-1, 1)

    GMM = GaussianMixture(
        n_components=n_components,
        covariance_type=covariance_type,
        reg_covar=reg_covar,
        max_iter=max_iter,
        random_state=random_state
    )

    GMM.fit(X)

    return GMM
