from __future__ import annotations

import numpy as np
def gmm_variances_1d(gmm):
    """
    Extract component variances from a 1D sklearn GaussianMixture.
    """

    if gmm.covariance_type == "full":
        variances = gmm.covariances_.reshape(-1)

    elif gmm.covariance_type == "diag":
        variances = gmm.covariances_.reshape(-1)

    elif gmm.covariance_type == "spherical":
        variances = gmm.covariances_.reshape(-1)

    elif gmm.covariance_type == "tied":
        variances = np.repeat(gmm.covariances_.reshape(-1)[0],
                              gmm.n_components)

    return variances
