from __future__ import annotations

import numpy as np
import pandas as pd
from weighted_quantile import *

def neutral_loss_gmm_table(mz_vec,
                           GMM,
                           stdDistance=3):
    """
    Convert a fitted GMM into a neutral-loss Gaussian object table.

    Uses raw mz observations and posterior probabilities.
    """

    mz_vec = np.asarray(mz_vec, dtype=float)
    mz_vec = mz_vec[np.isfinite(mz_vec)]

    X = mz_vec.reshape(-1, 1)

    Responsibilities = GMM.predict_proba(X)
    HardLabels = GMM.predict(X)

    means = GMM.means_.reshape(-1)

    if GMM.covariance_type == "full":
        variances = GMM.covariances_.reshape(-1)
    elif GMM.covariance_type == "diag":
        variances = GMM.covariances_.reshape(-1)
    elif GMM.covariance_type == "spherical":
        variances = GMM.covariances_.reshape(-1)
    elif GMM.covariance_type == "tied":
        variances = np.repeat(GMM.covariances_.reshape(-1)[0],
                              GMM.n_components)

    stds = np.sqrt(variances)
    weights = GMM.weights_

    rows = []

    for component_id in range(GMM.n_components):

        mz_mean = means[component_id]
        mz_std = stds[component_id]
        component_weight = weights[component_id]

        posterior_weights = Responsibilities[:, component_id]

        q25, q50, q75 = weighted_quantile(
            values=mz_vec,
            weights=posterior_weights,
            quantiles=[0.25, 0.50, 0.75]
        )

        iqr = q75 - q25

        hard_component_mz = mz_vec[HardLabels == component_id]

        rows.append({
            "neutral_loss_id": component_id,

            "neutral_loss_mz_(Da)": mz_mean,
            "neutral_loss_mz_std_(Da)": mz_std,
            "neutral_loss_mz_std_(ppm)": mz_std / mz_mean * 1e6,

            "Q25_mz_(Da)": q25,
            "median_mz_(Da)": q50,
            "Q75_mz_(Da)": q75,
            "IQR_mz_(Da)": iqr,
            "IQR_mz_(ppm)": iqr / mz_mean * 1e6,

            "mixture_weight": component_weight,
            "expected_support_count": np.sum(posterior_weights),
            "hard_support_count": len(hard_component_mz),

            "min_mz_(Da)": mz_mean - stdDistance * mz_std,
            "max_mz_(Da)": mz_mean + stdDistance * mz_std,

            "hard_min_mz_(Da)": np.min(hard_component_mz) if len(hard_component_mz) > 0 else np.nan,
            "hard_max_mz_(Da)": np.max(hard_component_mz) if len(hard_component_mz) > 0 else np.nan,
        })

    NeutralLossGMMDF = pd.DataFrame(rows)

    NeutralLossGMMDF = NeutralLossGMMDF.sort_values(
        "neutral_loss_mz_(Da)"
    )

    NeutralLossGMMDF = NeutralLossGMMDF.reset_index(drop=True)

    return NeutralLossGMMDF
