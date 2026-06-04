from __future__ import annotations

import numpy as np

def gaussian_chromatogram_params_template():
    """
    Return a complete params dictionary for the dictionary-based Gaussian
    chromatogram workflow.

    Edit these values before passing params to resolve_full_chromatogram().
    """

    return {
        "columns": {
            "rt_col": 2,
            "int_col": 1,
        },
        "chromatogram": {
            "std_distance": 3,
            "rt_tol": 5,
            "min_signals": 5,
        },
        "smoothing": {
            "std_distance": 1,
            "freq_std_distance": 1,
            "min_signal_fraction": 0.5,
            "max_signals": 100,
            "savgol_window_times": 2,
            "savgol_min_poly": 5,
            "min_poly": 3,
            "prominence": 1,
            "distance": 2,
        },
        "signal_clustering": {
            "use_observed_min_signal": True,
            "min_signal": 0,
        },
        "redistribution": {
            "auto_power_of_two": False,
        },
        "gaussian": {
            "std_distance": 3,
            "estimate_rt_from_weights": False,
            "constrain_peaks": True,
            "min_value": 1e-5,
            "n_select_seed": 5,
            "seed_generations": 5,
            "min_contribution_percent": 2,
            "show_error_chrom": False,
        },
        "selection": {
            "lower_std": 1e-2,
        },
        "curve_fit": {
            "maxfev": 10000,
        },
        "random": {
            "rng": np.random.default_rng(0),
        },
        "output": {
            "save_peaks": False,
            "output_folder": ".",
            "mz_name": "-mz",
        },
    }
