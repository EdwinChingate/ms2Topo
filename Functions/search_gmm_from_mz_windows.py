from __future__ import annotations

import numpy as np
import pandas as pd
from estimate_gmm_component_range import *
from search_neutral_loss_gmm_components import *
def search_gmm_from_mz_windows(neutral_losses_array,
                               mz_windows,
                               target_component_iqr_da,
                               min_points_per_component = 5,
                               max_components_cap = 20,
                               covariance_type = "full",
                               reg_covar = 1e-12,
                               max_iter = 1000,
                               random_state = 7):
    """
    Run local GMM searches from mz windows.

    Expected mz_windows columns:
        mz_windows[:, 0] = start_idx
        mz_windows[:, 1] = stop_idx
        mz_windows[:, 2] = IQR mz, Da
        mz_windows[:, 3] = IQR mz, ppm
    """

    rows = []
    gmm_models_dict = {}

    for window_id, window in enumerate(mz_windows):

        low_id_mz = int(window[0])
        high_id_mz = int(window[1])
        iqr_mz_da = window[2]
        iqr_mz_ppm = window[3]

        mz_vec = neutral_losses_array[low_id_mz: high_id_mz]
        mz_vec = np.asarray(mz_vec,
                            dtype = float)

        mz_vec = mz_vec[np.isfinite(mz_vec)]

        n_points = len(mz_vec)

        min_components, max_components = estimate_gmm_component_range(n_points = n_points,
                                                                      iqr_mz_da = iqr_mz_da,
                                                                      target_component_iqr_da = target_component_iqr_da,
                                                                      min_points_per_component = min_points_per_component,
                                                                      max_components_cap = max_components_cap)

        if max_components < 1:
            continue

        BestGMM, GMMSearchDF, ModelsDict = search_neutral_loss_gmm_components(mz_vec = mz_vec,
                                                                              min_components = min_components,
                                                                              max_components = max_components,
                                                                              covariance_type = covariance_type,
                                                                              reg_covar = reg_covar,
                                                                              max_iter = max_iter,
                                                                              random_state = random_state)

        rows.append({"window_id": window_id,
                     "start_idx": low_id_mz,
                     "stop_idx": high_id_mz,
                     "n_points": n_points,
                     "iqr_mz_da": iqr_mz_da,
                     "iqr_mz_ppm": iqr_mz_ppm,
                     "target_component_iqr_da": target_component_iqr_da,
                     "min_components": min_components,
                     "max_components": max_components,
                     "best_n_components": BestGMM.n_components,
                     "best_BIC": GMMSearchDF["BIC"].min(),
                     "best_AIC": GMMSearchDF["AIC"].min()})

        gmm_models_dict[window_id] = {"BestGMM": BestGMM,
                                      "GMMSearchDF": GMMSearchDF,
                                      "ModelsDict": ModelsDict,
                                      "mz_vec": mz_vec}

    return pd.DataFrame(rows), gmm_models_dict
