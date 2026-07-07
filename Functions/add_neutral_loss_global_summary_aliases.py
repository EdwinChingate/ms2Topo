# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import pandas as pd


def add_neutral_loss_global_summary_aliases(assignment_global_summary_df):
    """
    Add neutral-loss-specific count aliases to the global assignment summary.
    """

    if assignment_global_summary_df is None or len(assignment_global_summary_df) == 0:
        return pd.DataFrame()

    summary_df = assignment_global_summary_df.copy()

    alias_dict = {"n_loaded_positive_intensity_fragments": "n_generated_neutral_losses_tested",
                  "n_assigned_fragments": "n_assigned_neutral_losses",
                  "n_confident_fragments": "n_confident_neutral_losses",
                  "n_ambiguous_fragments": "n_ambiguous_neutral_losses",
                  "n_unassigned_fragments": "n_unassigned_neutral_losses",
                  "n_no_candidate_fragments": "n_neutral_losses_with_no_candidate_centroid",
                  "all_positive_intensity_fragments_assigned": "all_neutral_losses_assigned"}

    for old_col, new_col in alias_dict.items():
        if old_col in summary_df.columns:
            summary_df[new_col] = summary_df[old_col]

    return summary_df
