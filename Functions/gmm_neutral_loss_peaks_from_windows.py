# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import numpy as np
import pandas as pd
from calculate_target_iqr_da import calculate_target_iqr_da
from estimate_gmm_components_by_resampling import estimate_gmm_components_by_resampling
from estimate_max_gmm_components_from_mz_interval import estimate_max_gmm_components_from_mz_interval
from fit_neutral_loss_gmm_components import fit_neutral_loss_gmm_components
from gmm_variances_1d import gmm_variances_1d
from search_neutral_loss_gmm_components import search_neutral_loss_gmm_components


def gmm_neutral_loss_peaks_from_windows(neutral_losses_array,
                                        mz_windows,
                                        target_component_iqr_da = 1e-3,
                                        target_component_iqr_ppm = 3,
                                        min_counts = 3,
                                        min_points_per_component = None,
                                        min_component_separation_da = 1e-3,
                                        max_components_per_da = None,
                                        min_component_separation_ppm = 3,
                                        max_components_cap = 10,
                                        covariance_type = "full",
                                        reg_covar = (1e-5) ** 2,
                                        max_iter = 1000,
                                        random_state = 7,
                                        std_distance = 3,
                                        skip_gmm_for_tolerable_iqr = True,
                                        use_resampled_gmm = False,
                                        n_resampling_iterations = 30,
                                        current_sampling_size = 200,
                                        resampling_std_times = 1,
                                        assignment_window_padding_da = 0.0,
                                        assignment_window_padding_ppm = 0.0,
                                        return_gmm_resampling_diagnostics = False,
                                        return_component_cap_diagnostics = False):
    """
    Refine m/z windows with local GMMs and return an extended m/z-object table.

    The maximum number of GMM components is estimated from the m/z interval
    length and a component-density rule, not from Gaussian probability-density
    overlap.

    Component-density controls:
        min_component_separation_da
            Minimum distance in Da between two neighboring GMM means.

        max_components_per_da
            Optional reciprocal way to express the same rule:
                min_component_separation_da = 1 / max_components_per_da

        min_component_separation_ppm
            Optional ppm-scaled lower bound on component separation.

    If several controls are provided, the largest separation is used.

    Important coverage behavior:
        columns 19 and 20 contain observed assignment bounds for each component.
        These bounds are based on the actual m/z values assigned to the component,
        optionally padded. Use them as centroid_min_mz_col and centroid_max_mz_col
        during later alignment when you want the centroid vocabulary to preserve
        all fragments/neutral losses used to build it.

    Output columns:
        0  median mz
        1  count
        2  start index in input vector
        3  stop index in input vector, exclusive
        4  IQR mz, Da
        5  IQR mz, ppm
        6  Gaussian mz, Da
        7  Gaussian std, Da
        8  Gaussian std, ppm
        9  Gaussian min mz = Gaussian mz - std_distance * std
        10 Gaussian max mz = Gaussian mz + std_distance * std
        11 component weight
        12 expected count
        13 mean responsibility
        14 min responsibility
        15 local n components
        16 local BIC
        17 local AIC
        18 delta BIC vs one-component model
        19 assignment min mz, observed component bound with optional padding
        20 assignment max mz, observed component bound with optional padding
    """

    if target_component_iqr_da <= 0:
        raise ValueError("target_component_iqr_da must be > 0")

    if target_component_iqr_ppm <= 0:
        raise ValueError("target_component_iqr_ppm must be > 0")

    neutral_losses_array = np.asarray(neutral_losses_array,
                                      dtype = float)

    mz_windows = np.asarray(mz_windows,
                            dtype = float)

    rows = []
    component_cap_rows = []
    resampling_diagnostic_tables = []
    resampling_summary_tables = []

    for window_id, mz_window in enumerate(mz_windows):

        low_id_mz = int(mz_window[0])
        high_id_mz = int(mz_window[1])
        iqr_mz_da = float(mz_window[2])

        mz_vec = neutral_losses_array[low_id_mz: high_id_mz]

        mz_vec = np.asarray(mz_vec,
                            dtype = float)

        mz_vec = mz_vec[np.isfinite(mz_vec)]

        n_points = len(mz_vec)

        if n_points < min_counts:
            continue

        median_mz_window = float(np.median(mz_vec))

        target_iqr_da = calculate_target_iqr_da(median_mz = median_mz_window,
                                                target_component_iqr_da = target_component_iqr_da,
                                                target_component_iqr_ppm = target_component_iqr_ppm)

        cap_result = estimate_max_gmm_components_from_mz_interval(
            mz_vec = mz_vec,
            min_component_separation_da = min_component_separation_da,
            max_components_per_da = max_components_per_da,
            min_component_separation_ppm = min_component_separation_ppm,
            max_components_cap = max_components_cap,
            min_points_per_component = min_points_per_component)

        max_components = int(cap_result["max_components"])

        component_cap_rows.append({"window_id": int(window_id),
                                   "window_low_id_mz": int(low_id_mz),
                                   "window_high_id_mz": int(high_id_mz),
                                   "n_points": int(n_points),
                                   "window_iqr_da": float(iqr_mz_da),
                                   "target_iqr_da": float(target_iqr_da),
                                   "window_width_da": float(cap_result["window_width_da"]),
                                   "minimum_separation_da": float(cap_result["minimum_separation_da"]) if np.isfinite(cap_result["minimum_separation_da"]) else np.nan,
                                   "max_components_by_interval": int(cap_result["max_components_by_interval"]),
                                   "max_components_by_points": cap_result["max_components_by_points"],
                                   "max_components": int(max_components)})

        if skip_gmm_for_tolerable_iqr and iqr_mz_da <= target_iqr_da:

            median_mz = median_mz_window

            q1_mz = np.percentile(mz_vec,
                                  25)

            q3_mz = np.percentile(mz_vec,
                                  75)

            component_iqr_mz_da = q3_mz - q1_mz

            if median_mz != 0:

                component_iqr_mz_ppm = component_iqr_mz_da / median_mz * 1e6

            else:

                component_iqr_mz_ppm = np.nan

            gaussian_mz = np.mean(mz_vec)

            if n_points > 1:

                gaussian_std = np.std(mz_vec,
                                      ddof = 1)

            else:

                gaussian_std = 0.0

            gaussian_std = max(gaussian_std,
                               np.sqrt(reg_covar))

            if gaussian_mz != 0:

                gaussian_std_ppm = gaussian_std / gaussian_mz * 1e6

            else:

                gaussian_std_ppm = np.nan

            gaussian_min_mz = gaussian_mz - std_distance * gaussian_std
            gaussian_max_mz = gaussian_mz + std_distance * gaussian_std

            assignment_padding = max(float(assignment_window_padding_da),
                                     float(assignment_window_padding_ppm) / 1e6 * median_mz)

            assignment_min_mz = np.min(mz_vec) - assignment_padding
            assignment_max_mz = np.max(mz_vec) + assignment_padding

            rows.append([median_mz,
                         n_points,
                         low_id_mz,
                         high_id_mz,
                         component_iqr_mz_da,
                         component_iqr_mz_ppm,
                         gaussian_mz,
                         gaussian_std,
                         gaussian_std_ppm,
                         gaussian_min_mz,
                         gaussian_max_mz,
                         1.0,
                         float(n_points),
                         1.0,
                         1.0,
                         1,
                         np.nan,
                         np.nan,
                         np.nan,
                         assignment_min_mz,
                         assignment_max_mz])

            continue

        if max_components <= 1:

            best_gmm = fit_neutral_loss_gmm_components(mz_vec = mz_vec,
                                                       n_components = 1,
                                                       covariance_type = covariance_type,
                                                       reg_covar = reg_covar,
                                                       max_iter = max_iter,
                                                       random_state = random_state)

            x_for_bic = mz_vec.reshape(-1, 1)

            local_bic = float(best_gmm.bic(x_for_bic))
            local_aic = float(best_gmm.aic(x_for_bic))
            one_component_bic = local_bic

        elif use_resampled_gmm:

            resampling_result = estimate_gmm_components_by_resampling(
                mz_vec = mz_vec,
                min_components = 1,
                max_components = max_components,
                n_iterations = n_resampling_iterations,
                current_sampling_size = current_sampling_size,
                min_points_per_component = min_points_per_component,
                std_times = resampling_std_times,
                covariance_type = covariance_type,
                reg_covar = reg_covar,
                max_iter = max_iter,
                random_state = random_state + window_id)

            best_gmm = resampling_result["final_gmm"]
            selected_n_components = int(resampling_result["selected_n_components"])
            gmm_summary_df = resampling_result["gmm_resampling_summary_df"]

            local_bic = float(gmm_summary_df.loc[gmm_summary_df["n_components"] == selected_n_components,
                                                 "mean_BIC"].iloc[0])

            local_aic = float(gmm_summary_df.loc[gmm_summary_df["n_components"] == selected_n_components,
                                                 "mean_AIC"].iloc[0])

            if 1 in gmm_summary_df["n_components"].to_numpy(dtype = int):

                one_component_bic = float(gmm_summary_df.loc[gmm_summary_df["n_components"] == 1,
                                                             "mean_BIC"].iloc[0])

            else:

                one_component_bic = np.nan

            if return_gmm_resampling_diagnostics:

                current_resampling_df = resampling_result["gmm_resampling_df"].copy()
                current_resampling_df.insert(0,
                                             "window_id",
                                             int(window_id))
                current_resampling_df.insert(1,
                                             "window_low_id_mz",
                                             int(low_id_mz))
                current_resampling_df.insert(2,
                                             "window_high_id_mz",
                                             int(high_id_mz))

                current_summary_df = gmm_summary_df.copy()
                current_summary_df.insert(0,
                                          "window_id",
                                          int(window_id))
                current_summary_df.insert(1,
                                          "window_low_id_mz",
                                          int(low_id_mz))
                current_summary_df.insert(2,
                                          "window_high_id_mz",
                                          int(high_id_mz))

                resampling_diagnostic_tables.append(current_resampling_df)
                resampling_summary_tables.append(current_summary_df)

        else:

            best_gmm, gmm_search_df, models_dict = search_neutral_loss_gmm_components(
                mz_vec = mz_vec,
                min_components = 1,
                max_components = max_components,
                covariance_type = covariance_type,
                reg_covar = reg_covar,
                max_iter = max_iter,
                random_state = random_state)

            local_bic = float(np.min(gmm_search_df["BIC"]))
            local_aic = float(np.min(gmm_search_df["AIC"]))

            one_component_bic = float(gmm_search_df.loc[gmm_search_df["n_components"] == 1,
                                                        "BIC"].iloc[0])

        delta_bic_vs_one = local_bic - one_component_bic

        x = mz_vec.reshape(-1, 1)

        labels = best_gmm.predict(x)
        responsibilities = best_gmm.predict_proba(x)

        gaussian_mz_vec = best_gmm.means_.reshape(-1)
        gaussian_std_vec = np.sqrt(gmm_variances_1d(best_gmm))
        component_weight_vec = best_gmm.weights_

        for component_id in range(best_gmm.n_components):

            component_local_ids = np.where(labels == component_id)[0]

            if len(component_local_ids) < min_counts:
                continue

            component_mz_vec = mz_vec[component_local_ids]

            component_mz_vec = np.asarray(component_mz_vec,
                                          dtype = float)

            component_mz_vec = component_mz_vec[np.isfinite(component_mz_vec)]

            if len(component_mz_vec) < min_counts:
                continue

            component_start_idx = low_id_mz + int(np.min(component_local_ids))
            component_stop_idx = low_id_mz + int(np.max(component_local_ids)) + 1

            median_mz = np.median(component_mz_vec)

            q1_mz = np.percentile(component_mz_vec,
                                  25)

            q3_mz = np.percentile(component_mz_vec,
                                  75)

            component_iqr_mz_da = q3_mz - q1_mz

            if median_mz != 0:

                component_iqr_mz_ppm = component_iqr_mz_da / median_mz * 1e6

            else:

                component_iqr_mz_ppm = np.nan

            gaussian_mz = gaussian_mz_vec[component_id]
            gaussian_std = gaussian_std_vec[component_id]

            if gaussian_mz != 0:

                gaussian_std_ppm = gaussian_std / gaussian_mz * 1e6

            else:

                gaussian_std_ppm = np.nan

            gaussian_min_mz = gaussian_mz - std_distance * gaussian_std
            gaussian_max_mz = gaussian_mz + std_distance * gaussian_std

            component_responsibility_vec = responsibilities[component_local_ids,
                                                            component_id]

            expected_count = np.sum(responsibilities[:, component_id])
            mean_responsibility = np.mean(component_responsibility_vec)
            min_responsibility = np.min(component_responsibility_vec)

            assignment_padding = max(float(assignment_window_padding_da),
                                     float(assignment_window_padding_ppm) / 1e6 * median_mz)

            assignment_min_mz = np.min(component_mz_vec) - assignment_padding
            assignment_max_mz = np.max(component_mz_vec) + assignment_padding

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
                         delta_bic_vs_one,
                         assignment_min_mz,
                         assignment_max_mz])

    if len(rows) == 0:

        neutral_loss_gmm_peaks = np.zeros((0, 21))

    else:

        neutral_loss_gmm_peaks = np.array(rows,
                                          dtype = float)

        neutral_loss_gmm_peaks = neutral_loss_gmm_peaks[neutral_loss_gmm_peaks[:, 0].argsort(), :]

    if not return_gmm_resampling_diagnostics and not return_component_cap_diagnostics:

        return neutral_loss_gmm_peaks

    result = {"neutral_loss_gmm_peaks": neutral_loss_gmm_peaks}

    if return_gmm_resampling_diagnostics:

        if len(resampling_diagnostic_tables) > 0:

            gmm_resampling_df = pd.concat(resampling_diagnostic_tables,
                                          axis = 0,
                                          ignore_index = True)

        else:

            gmm_resampling_df = pd.DataFrame()

        if len(resampling_summary_tables) > 0:

            gmm_resampling_summary_df = pd.concat(resampling_summary_tables,
                                                  axis = 0,
                                                  ignore_index = True)

        else:

            gmm_resampling_summary_df = pd.DataFrame()

        result["gmm_resampling_df"] = gmm_resampling_df
        result["gmm_resampling_summary_df"] = gmm_resampling_summary_df

    if return_component_cap_diagnostics:

        result["component_cap_diagnostic_df"] = pd.DataFrame(component_cap_rows)

    return result
