# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import numpy as np
import pandas as pd
from fit_neutral_loss_gmm_components import fit_neutral_loss_gmm_components
from score_neutral_loss_gmm_components import score_neutral_loss_gmm_components
from summarize_resampled_gmm_search import summarize_resampled_gmm_search


def estimate_gmm_components_by_resampling(mz_vec,
                                          min_components = 1,
                                          max_components = 100,
                                          n_iterations = 30,
                                          current_sampling_size = 200,
                                          min_points_per_component = None,
                                          std_times = 1,
                                          covariance_type = "full",
                                          reg_covar = 1e-12,
                                          max_iter = 1000,
                                          random_state = 7):
    """
    Estimate a stable number of GMM components by repeated random subsampling.

    The maximum component count should already be constrained by an m/z interval
    and component-density rule before this function is called.

    This function estimates n_components only. The returned final_gmm is fitted
    on the full mz_vec using the selected n_components.
    """

    mz_vec = np.asarray(mz_vec,
                        dtype = float)

    mz_vec = mz_vec[np.isfinite(mz_vec)]

    n_points = len(mz_vec)

    if n_points == 0:
        raise ValueError("mz_vec has no finite values.")

    min_components = max(int(min_components),
                         1)

    max_components = min(int(max_components),
                         n_points)

    max_components = max(max_components,
                         min_components)

    current_sampling_size = min(int(current_sampling_size),
                                n_points)

    current_sampling_size = max(current_sampling_size,
                                1)

    if min_points_per_component is not None:

        max_components_by_sample_size = current_sampling_size // max(int(min_points_per_component),
                                                                     1)

        max_components_by_sample_size = max(max_components_by_sample_size,
                                            1)

        max_components = min(max_components,
                             max_components_by_sample_size)

    if max_components <= 1 or n_points == 1:

        final_gmm = fit_neutral_loss_gmm_components(mz_vec = mz_vec,
                                                    n_components = 1,
                                                    covariance_type = covariance_type,
                                                    reg_covar = reg_covar,
                                                    max_iter = max_iter,
                                                    random_state = random_state)

        X = mz_vec.reshape(-1, 1)

        bic_value = float(final_gmm.bic(X))
        aic_value = float(final_gmm.aic(X))

        gmm_resampling_df = pd.DataFrame([{"iteration": 0,
                                           "sample_size": int(n_points),
                                           "n_components": 1,
                                           "BIC": bic_value,
                                           "AIC": aic_value,
                                           "converged": bool(final_gmm.converged_),
                                           "n_iter": int(final_gmm.n_iter_),
                                           "selected_in_iteration": True}])

        gmm_resampling_summary_df = pd.DataFrame([{"n_components": 1,
                                                   "mean_BIC": bic_value,
                                                   "std_BIC": 0.0,
                                                   "median_BIC": bic_value,
                                                   "mean_AIC": aic_value,
                                                   "std_AIC": 0.0,
                                                   "median_AIC": aic_value,
                                                   "n_evaluations": 1,
                                                   "n_selected_by_iteration": 1,
                                                   "lower_BIC": bic_value,
                                                   "upper_BIC": bic_value,
                                                   "plausible_by_BIC": True,
                                                   "selected_n_components": 1}])

        return {"final_gmm": final_gmm,
                "selected_n_components": 1,
                "gmm_resampling_df": gmm_resampling_df,
                "gmm_resampling_summary_df": gmm_resampling_summary_df,
                "sampled_point_ids_by_iteration": [np.arange(n_points,
                                                             dtype = int)]}

    if n_points <= current_sampling_size:
        n_iterations = 1

    rng = np.random.default_rng(random_state)

    gmm_resampling_rows = []
    sampled_point_ids_by_iteration = []

    for iteration in range(int(n_iterations)):

        if current_sampling_size >= n_points:

            sampled_point_ids = np.arange(n_points,
                                          dtype = int)

        else:

            sampled_point_ids = rng.choice(np.arange(n_points),
                                           size = current_sampling_size,
                                           replace = False)

            sampled_point_ids = np.sort(sampled_point_ids)

        sampled_point_ids_by_iteration.append(sampled_point_ids)

        sampled_mz_vec = mz_vec[sampled_point_ids]

        gmm_search_df, selected_in_iteration = score_neutral_loss_gmm_components(
            mz_vec = sampled_mz_vec,
            min_components = min_components,
            max_components = max_components,
            covariance_type = covariance_type,
            reg_covar = reg_covar,
            max_iter = max_iter,
            random_state = random_state + iteration)

        for row_id in range(len(gmm_search_df)):

            row = gmm_search_df.iloc[row_id].to_dict()

            gmm_resampling_rows.append({"iteration": int(iteration),
                                        "sample_size": int(len(sampled_mz_vec)),
                                        "n_components": int(row["n_components"]),
                                        "BIC": float(row["BIC"]),
                                        "AIC": float(row["AIC"]),
                                        "converged": bool(row["converged"]),
                                        "n_iter": int(row["n_iter"]),
                                        "selected_in_iteration": int(row["n_components"]) == int(selected_in_iteration)})

    summary_result = summarize_resampled_gmm_search(gmm_resampling_rows = gmm_resampling_rows,
                                                    std_times = std_times)

    selected_n_components = int(summary_result["selected_n_components"])

    final_gmm = fit_neutral_loss_gmm_components(mz_vec = mz_vec,
                                                n_components = selected_n_components,
                                                covariance_type = covariance_type,
                                                reg_covar = reg_covar,
                                                max_iter = max_iter,
                                                random_state = random_state)

    return {"final_gmm": final_gmm,
            "selected_n_components": selected_n_components,
            "gmm_resampling_df": pd.DataFrame(gmm_resampling_rows),
            "gmm_resampling_summary_df": summary_result["gmm_resampling_summary_df"],
            "sampled_point_ids_by_iteration": sampled_point_ids_by_iteration}
