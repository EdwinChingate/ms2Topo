from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture

def search_neutral_loss_gmm_components(mz_vec,
                                       min_components=1,
                                       max_components=100,
                                       covariance_type="full",
                                       reg_covar=1e-12,
                                       max_iter=1000,
                                       random_state=7):
    """
    Fit several Gaussian mixture models and select the one with lowest BIC.
    """

    mz_vec = np.asarray(mz_vec, dtype=float)
    mz_vec = mz_vec[np.isfinite(mz_vec)]

    X = mz_vec.reshape(-1, 1)

    rows = []
    ModelsDict = {}

    for n_components in range(min_components, max_components + 1):

        GMM = GaussianMixture(
            n_components=n_components,
            covariance_type=covariance_type,
            reg_covar=reg_covar,
            max_iter=max_iter,
            random_state=random_state
        )

        GMM.fit(X)

        bic = GMM.bic(X)
        aic = GMM.aic(X)

        rows.append({
            "n_components": n_components,
            "BIC": bic,
            "AIC": aic,
            "converged": GMM.converged_,
            "n_iter": GMM.n_iter_
        })

        ModelsDict[n_components] = GMM

    GMMSearchDF = pd.DataFrame(rows)

    best_n_components = int(
        GMMSearchDF.loc[GMMSearchDF["BIC"].idxmin(), "n_components"]
    )

    BestGMM = ModelsDict[best_n_components]

    return BestGMM, GMMSearchDF, ModelsDict
