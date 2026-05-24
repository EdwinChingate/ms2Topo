from __future__ import annotations

from expected_ion_mz_from_formula import *

# TODO: unresolved names: col

def search_features_by_formula(features_table_df,
                               formula,
                               ionization_mode = "positive",
                               adduct = None,
                               mz_col = "median_mz(Da)",
                               id_cols = None,
                               ppm_tol = 5.0,
                               top_n = 10,
                               only_within_tolerance = True,
                               keep_sample_columns = True):
    """
    Search an ms2Topo feature table for features close to the expected precursor
    m/z calculated from a molecular formula and ionization mode.

    Returns feature IDs together with mass-error diagnostics.
    """

    if mz_col not in features_table_df.columns:
        raise ValueError(f"mz_col='{mz_col}' was not found. Available columns are: "
                         f"{list(features_table_df.columns)}")

    if id_cols is None:
        id_cols = ["feat_id",
                   "Unnamed: 0"]

    id_cols = [col for col in id_cols if col in features_table_df.columns]

    ion_info = expected_ion_mz_from_formula(formula = formula,
                                            ionization_mode = ionization_mode,
                                            adduct = adduct)

    expected_mz = ion_info["expected_mz"]

    results_df = features_table_df.copy()

    results_df["query_formula"] = ion_info["formula"]
    results_df["neutral_exact_mass"] = ion_info["neutral_exact_mass"]
    results_df["ionization_mode"] = ion_info["ionization_mode"]
    results_df["adduct"] = ion_info["adduct"]
    results_df["expected_mz"] = expected_mz

    results_df["mz_error_da"] = results_df[mz_col].astype(float) - expected_mz
    results_df["mz_error_ppm"] = results_df["mz_error_da"] / expected_mz * 1e6
    results_df["abs_mz_error_da"] = results_df["mz_error_da"].abs()
    results_df["abs_mz_error_ppm"] = results_df["mz_error_ppm"].abs()
    results_df["within_ppm_tolerance"] = results_df["abs_mz_error_ppm"] <= ppm_tol

    if {"min_mz", "max_mz"}.issubset(results_df.columns):
        results_df["expected_mz_inside_feature_range"] = (results_df["min_mz"] <= expected_mz) & \
                                                        (results_df["max_mz"] >= expected_mz)

    results_df = results_df.sort_values("abs_mz_error_ppm").reset_index(drop = True)

    if only_within_tolerance:
        results_df = results_df[results_df["within_ppm_tolerance"]].copy()

    results_df = results_df.head(top_n).reset_index(drop = True)

    if not keep_sample_columns:
        sample_like_cols = [col for col in results_df.columns if str(col).isdigit()]

        results_df = results_df.drop(columns = sample_like_cols)

    preferred_first_cols = id_cols + [mz_col,
                                      "expected_mz",
                                      "mz_error_da",
                                      "mz_error_ppm",
                                      "abs_mz_error_ppm",
                                      "within_ppm_tolerance",
                                      "expected_mz_inside_feature_range",
                                      "query_formula",
                                      "neutral_exact_mass",
                                      "ionization_mode",
                                      "adduct",
                                      "median_RT(s)",
                                      "Q1_RT(s)",
                                      "Q3_RT(s)",
                                      "N_samples",
                                      "N_ms2-spectra",
                                      "median_silhouette",
                                      "median_intramodule_cosine"]

    preferred_first_cols = [col for col in preferred_first_cols if col in results_df.columns]

    remaining_cols = [col for col in results_df.columns if col not in preferred_first_cols]

    results_df = results_df[preferred_first_cols + remaining_cols]

    return results_df
                