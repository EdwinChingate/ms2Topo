from __future__ import annotations

import numpy as np
from gmm_variances_1d import *
from search_neutral_loss_gmm_components import *
def gmm_neutral_loss_peaks_from_windows(neutral_losses_array,
                                        mz_windows,
                                        target_component_iqr_da,
                                        min_counts = 3,
                                        min_points_per_component = 5,
                                        max_components_cap = 10,
                                        covariance_type = "full",
                                        reg_covar = (1e-5)**2,
                                        max_iter = 1000,
                                        random_state = 7,
                                        std_distance = 3):
    """
    Refine mz windows with local GMMs and return an extended mz-object table.

    Output:
        neutral_loss_gmm_peaks[:, 0]  = median mz
        neutral_loss_gmm_peaks[:, 1]  = count
        neutral_loss_gmm_peaks[:, 2]  = start index
        neutral_loss_gmm_peaks[:, 3]  = stop index, exclusive
        neutral_loss_gmm_peaks[:, 4]  = IQR mz, Da
        neutral_loss_gmm_peaks[:, 5]  = IQR mz, ppm

        neutral_loss_gmm_peaks[:, 6]  = Gaussian mz, Da
        neutral_loss_gmm_peaks[:, 7]  = Gaussian std, Da
        neutral_loss_gmm_peaks[:, 8]  = Gaussian std, ppm
        neutral_loss_gmm_peaks[:, 9]  = Gaussian min mz, mean - std_distance * std
        neutral_loss_gmm_peaks[:, 10] = Gaussian max mz, mean + std_distance * std

        neutral_loss_gmm_peaks[:, 11] = component weight
        neutral_loss_gmm_peaks[:, 12] = expected count
        neutral_loss_gmm_peaks[:, 13] = mean responsibility
        neutral_loss_gmm_peaks[:, 14] = min responsibility

        neutral_loss_gmm_peaks[:, 15] = local n components
        neutral_loss_gmm_peaks[:, 16] = local BIC
        neutral_loss_gmm_peaks[:, 17] = local AIC
        neutral_loss_gmm_peaks[:, 18] = delta BIC vs one-component model
    """

    rows = []

    for window_id, mz_window in enumerate(mz_windows):

        low_id_mz = int(mz_window[0])
        high_id_mz = int(mz_window[1])
        iqr_mz_da = mz_window[2]

        mz_vec = neutral_losses_array[low_id_mz: high_id_mz]

        mz_vec = np.asarray(mz_vec,
                            dtype = float)

        mz_vec = mz_vec[np.isfinite(mz_vec)]

        n_points = len(mz_vec)

        if n_points < min_counts:
            continue

        if target_component_iqr_da <= 0:
            raise ValueError("target_component_iqr_da must be > 0")

        max_by_points = n_points // min_points_per_component

        if iqr_mz_da <= 0:
            max_by_iqr = 1
        else:
            max_by_iqr = int(np.ceil(iqr_mz_da / target_component_iqr_da))

        max_components = min(max_by_points,
                             max_by_iqr,
                             max_components_cap)

        max_components = max(max_components,
                             1)

        best_gmm, gmm_search_df, models_dict = search_neutral_loss_gmm_components(mz_vec = mz_vec,
                                                                                  min_components = 1,
                                                                                  max_components = max_components,
                                                                                  covariance_type = covariance_type,
                                                                                  reg_covar = reg_covar,
                                                                                  max_iter = max_iter,
                                                                                  random_state = random_state)

        x = mz_vec.reshape(-1, 1)

        labels = best_gmm.predict(x)
        responsibilities = best_gmm.predict_proba(x)

        gaussian_mz_vec = best_gmm.means_.reshape(-1)
        gaussian_std_vec = np.sqrt(gmm_variances_1d(best_gmm))
        component_weight_vec = best_gmm.weights_

        local_bic = np.min(gmm_search_df["BIC"])
        local_aic = np.min(gmm_search_df["AIC"])

        one_component_bic = gmm_search_df.loc[gmm_search_df["n_components"] == 1,
                                              "BIC"].iloc[0]

        delta_bic_vs_one = local_bic - one_component_bic

        for component_id in range(best_gmm.n_components):

            component_local_ids = np.where(labels == component_id)[0]

            if len(component_local_ids) < min_counts:
                continue

            component_start_idx = low_id_mz + int(np.min(component_local_ids))
            component_stop_idx = low_id_mz + int(np.max(component_local_ids)) + 1

            component_mz_vec = neutral_losses_array[component_start_idx: component_stop_idx]

            component_mz_vec = np.asarray(component_mz_vec,
                                          dtype = float)

            component_mz_vec = component_mz_vec[np.isfinite(component_mz_vec)]

            if len(component_mz_vec) < min_counts:
                continue

            median_mz = np.median(component_mz_vec)

            q1_mz = np.percentile(component_mz_vec,
                                  25)

            q3_mz = np.percentile(component_mz_vec,
                                  75)

            component_iqr_mz_da = q3_mz - q1_mz
            component_iqr_mz_ppm = component_iqr_mz_da / median_mz * 1e6

            gaussian_mz = gaussian_mz_vec[component_id]
            gaussian_std = gaussian_std_vec[component_id]
            gaussian_std_ppm = gaussian_std / gaussian_mz * 1e6

            gaussian_min_mz = gaussian_mz - std_distance * gaussian_std
            gaussian_max_mz = gaussian_mz + std_distance * gaussian_std

            component_responsibility_vec = responsibilities[component_local_ids,
                                                            component_id]

            expected_count = np.sum(responsibilities[:, component_id])
            mean_responsibility = np.mean(component_responsibility_vec)
            min_responsibility = np.min(component_responsibility_vec)

            rows.append([median_mz,
                         len(component_mz_vec),
                         component_start_idx,
                         component_stop_idx,
                         component_iqr_mz_da,
                         component_iqr_mz_ppm,
                         gaussian_mz,
                         gaussian_std,
                         gaussian_std_ppm,
                         gaussian_min_mz,
                         gaussian_max_mz,
                         component_weight_vec[component_id],
                         expected_count,
                         mean_responsibility,
                         min_responsibility,
                         best_gmm.n_components,
                         local_bic,
                         local_aic,
                         delta_bic_vs_one])

    if len(rows) == 0:
        return np.zeros((0, 19))

    neutral_loss_gmm_peaks = np.array(rows,
                                      dtype = float)

    neutral_loss_gmm_peaks = neutral_loss_gmm_peaks[neutral_loss_gmm_peaks[:, 0].argsort(), :]

    return neutral_loss_gmm_peaks
