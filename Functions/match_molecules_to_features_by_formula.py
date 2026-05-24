from __future__ import annotations

import numpy as np
import pandas as pd
from clean_feat_id import *
from search_features_by_formula import *

# TODO: unresolved names: feat_id

def match_molecules_to_features_by_formula(features_table_df,
                                           molecules_df,
                                           formula_col = "molecular_formula",
                                           feat_id_col = "feat_id",
                                           ionization_mode = "positive",
                                           adduct = "[M+H]+",
                                           ppm_tol = 2,
                                           top_n = 2,
                                           mz_col = "median_mz(Da)",
                                           id_cols = None,
                                           keep_sample_columns = True,
                                           assign_only_within_tolerance = True):
    """
    Match molecular formulas to the closest features in an ms2Topo features table.

    The function uses search_features_by_formula for each molecular formula,
    assigns the closest feature ID to molecules_df, and returns the matched
    feature rows for downstream analysis.
    """

    if formula_col not in molecules_df.columns:
        raise ValueError(f"formula_col='{formula_col}' was not found in molecules_df.")

    if feat_id_col not in features_table_df.columns:
        raise ValueError(f"feat_id_col='{feat_id_col}' was not found in features_table_df.")

    if id_cols is None:
        id_cols = [feat_id_col,
                   "Unnamed: 0"]

    updated_molecules_df = molecules_df.copy()

    updated_molecules_df[feat_id_col] = None
    updated_molecules_df["feature_match_status"] = None
    updated_molecules_df["expected_mz"] = np.nan
    updated_molecules_df["matched_mz"] = np.nan
    updated_molecules_df["mz_error_da"] = np.nan
    updated_molecules_df["mz_error_ppm"] = np.nan
    updated_molecules_df["abs_mz_error_ppm"] = np.nan
    updated_molecules_df["within_ppm_tolerance"] = np.nan

    candidate_hits = []
    matched_feature_rows = []

    for molecule_index, molecule_row in molecules_df.iterrows():
        formula = molecule_row[formula_col]

        if pd.isna(formula):
            updated_molecules_df.loc[molecule_index,
                                     "feature_match_status"] = "missing_formula"
            continue

        try:
            hits_df = search_features_by_formula(features_table_df = features_table_df,
                                                 formula = formula,
                                                 ionization_mode = ionization_mode,
                                                 adduct = adduct,
                                                 mz_col = mz_col,
                                                 id_cols = id_cols,
                                                 ppm_tol = ppm_tol,
                                                 top_n = top_n,
                                                 only_within_tolerance = False,
                                                 keep_sample_columns = keep_sample_columns)

            if len(hits_df) == 0:
                updated_molecules_df.loc[molecule_index,
                                         "feature_match_status"] = "no_feature_found"
                continue

            hits_df = hits_df.copy()

            hits_df["molecule_index"] = molecule_index
            hits_df["molecule_formula"] = formula
            hits_df["candidate_rank"] = np.arange(1,
                                                  len(hits_df) + 1,
                                                  dtype = int)

            candidate_hits.append(hits_df)

            closest_hit = hits_df.iloc[0].copy()

            within_ppm_tolerance = bool(closest_hit["within_ppm_tolerance"])

            if assign_only_within_tolerance and not within_ppm_tolerance:
                matched_feat_id = None
                match_status = "closest_outside_tolerance"

            else:
                matched_feat_id = clean_feat_id(closest_hit[feat_id_col])
                match_status = "matched"

            updated_molecules_df.loc[molecule_index,
                                     feat_id_col] = matched_feat_id

            updated_molecules_df.loc[molecule_index,
                                     "feature_match_status"] = match_status

            updated_molecules_df.loc[molecule_index,
                                     "expected_mz"] = closest_hit["expected_mz"]

            updated_molecules_df.loc[molecule_index,
                                     "matched_mz"] = closest_hit[mz_col]

            updated_molecules_df.loc[molecule_index,
                                     "mz_error_da"] = closest_hit["mz_error_da"]

            updated_molecules_df.loc[molecule_index,
                                     "mz_error_ppm"] = closest_hit["mz_error_ppm"]

            updated_molecules_df.loc[molecule_index,
                                     "abs_mz_error_ppm"] = closest_hit["abs_mz_error_ppm"]

            updated_molecules_df.loc[molecule_index,
                                     "within_ppm_tolerance"] = within_ppm_tolerance

            closest_hit["feature_match_status"] = match_status
            closest_hit[feat_id_col] = matched_feat_id

            matched_feature_rows.append(closest_hit)

        except Exception as error:
            updated_molecules_df.loc[molecule_index,
                                     "feature_match_status"] = f"failed: {error}"

    if len(candidate_hits) > 0:
        candidate_hits_df = pd.concat(candidate_hits,
                                      axis = 0,
                                      ignore_index = True)

    else:
        candidate_hits_df = pd.DataFrame()

    if len(matched_feature_rows) > 0:
        matched_features_df = pd.DataFrame(matched_feature_rows).reset_index(drop = True)

    else:
        matched_features_df = pd.DataFrame()

    matched_feat_ids = [clean_feat_id(feat_id) for feat_id in updated_molecules_df[feat_id_col]
                        if clean_feat_id(feat_id) is not None]

    matched_feat_ids = pd.unique(matched_feat_ids).tolist()

    features_feat_id_vec = features_table_df[feat_id_col].apply(clean_feat_id)

    features_subset_df = features_table_df.loc[
        features_feat_id_vec.isin(matched_feat_ids)
    ].copy()

    return {"molecules_df": updated_molecules_df,
            "matched_features_df": matched_features_df,
            "candidate_hits_df": candidate_hits_df,
            "features_subset_df": features_subset_df,
            "matched_feat_ids": matched_feat_ids}
            
from __future__ import annotations