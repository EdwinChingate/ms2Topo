# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import numpy as np
from sklearn.mixture import GaussianMixture


def fit_neutral_loss_gmm_components(mz_vec,
                                    n_components,
                                    covariance_type = "full",
                                    reg_covar = 1e-12,
                                    max_iter = 1000,
                                    random_state = 7):
    """
    Fit a 1D GaussianMixture with a fixed number of components.

    This helper is used after a component-count rule has selected the component
    count. The final GMM is fitted on the full m/z vector, not on a subsample.
    """

    mz_vec = np.asarray(mz_vec,
                        dtype = float)

    mz_vec = mz_vec[np.isfinite(mz_vec)]

    if len(mz_vec) == 0:
        raise ValueError("mz_vec has no finite values.")

    n_components = int(n_components)

    if n_components < 1:
        raise ValueError("n_components must be >= 1.")

    if n_components > len(mz_vec):
        raise ValueError("n_components cannot be larger than len(mz_vec).")

    X = mz_vec.reshape(-1, 1)

    gmm = GaussianMixture(n_components = n_components,
                          covariance_type = covariance_type,
                          reg_covar = reg_covar,
                          max_iter = max_iter,
                          random_state = random_state)

    gmm.fit(X)

    return gmm
