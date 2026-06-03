from __future__ import annotations

import pandas as pd
from prepare_aligned_annotation_matrix import *

def combine_aligned_annotation_matrices(aligned_matrices_dict,
                                        fill_value = 0,
                                        binary_matrix = True,
                                        sort_columns = True,
                                        return_diagnostics = True):
    """
    Combine several aligned annotation matrices before Tanimoto calculation.

    Parameters
    ----------
    aligned_matrices_dict:
        Dictionary where keys are annotation types and values are aligned
        matrices.

        Example:
            {
                "fragment": aligned_fragments_df,
                "loss": aligned_losses_df,
                "transition": aligned_transitions_df
            }

    Output
    ------
    combined_df:
        Matrix with:
            rows    -> prefixed annotation IDs
            columns -> normalized feat_id
            values  -> binary or numeric annotation values
    """

    if not isinstance(aligned_matrices_dict, dict):
        raise TypeError("aligned_matrices_dict must be a dictionary.")

    if len(aligned_matrices_dict) == 0:
        raise ValueError("aligned_matrices_dict is empty.")

    prepared_matrices = []
    diagnostics_rows = []

    for annotation_type, aligned_matrix_df in aligned_matrices_dict.items():

        prepared_df = prepare_aligned_annotation_matrix(
            aligned_matrix_df = aligned_matrix_df,
            annotation_type = annotation_type,
            fill_value = fill_value,
            binary_matrix = binary_matrix
        )

        prepared_matrices.append(prepared_df)

        diagnostics_rows.append({
            "annotation_type": annotation_type,
            "n_rows": prepared_df.shape[0],
            "n_columns": prepared_df.shape[1],
            "n_nonzero_values": int((prepared_df > fill_value).sum().sum())
        })

    all_columns = sorted(set().union(*[set(df.columns) for df in prepared_matrices]))

    if not sort_columns:
        all_columns = list(set().union(*[set(df.columns) for df in prepared_matrices]))

    prepared_matrices = [df.reindex(columns = all_columns,
                                    fill_value = fill_value)
                         for df in prepared_matrices]

    combined_df = pd.concat(prepared_matrices,
                            axis = 0)

    if combined_df.index.duplicated().any():
        duplicated_rows = list(combined_df.index[combined_df.index.duplicated()].unique())

        raise ValueError("Duplicated annotation IDs were found after prefixing. "
                         f"Duplicated rows: {duplicated_rows[:20]}")

    if binary_matrix:
        combined_df = (combined_df > fill_value).astype(int)

    diagnostics_df = pd.DataFrame(diagnostics_rows)

    diagnostics_df.loc[len(diagnostics_df)] = {
        "annotation_type": "combined",
        "n_rows": combined_df.shape[0],
        "n_columns": combined_df.shape[1],
        "n_nonzero_values": int((combined_df > fill_value).sum().sum())
    }

    if return_diagnostics:
        return combined_df, diagnostics_df

    return combined_df
