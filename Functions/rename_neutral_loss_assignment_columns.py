# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import pandas as pd


def rename_neutral_loss_assignment_columns(table):
    """
    Return a neutral-loss-language copy of an assignment diagnostic table.

    The shared assignment core still produces fragment-oriented column names.
    This helper makes the neutral-loss top-level output easier to read without
    changing the reusable assignment core.
    """

    if table is None or len(table) == 0:
        return pd.DataFrame()

    rename_dict = {"fragment_id_in_spectrum": "neutral_loss_id_in_spectrum",
                   "fragment_mz": "neutral_loss_mz",
                   "fragment_intensity": "neutral_loss_presence",
                   "raw_fragment_intensity": "raw_neutral_loss_presence",
                   "assigned_fragment_id": "assigned_neutral_loss_id",
                   "assigned_fragment_mz": "assigned_neutral_loss_mz",
                   "n_candidate_fragments": "n_candidate_neutral_losses"}

    available_rename_dict = {old_col: new_col
                             for old_col, new_col in rename_dict.items()
                             if old_col in table.columns}

    return table.rename(columns = available_rename_dict).copy()
