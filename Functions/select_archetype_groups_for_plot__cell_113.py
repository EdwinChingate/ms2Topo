from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import textwrap

def select_archetype_groups_for_plot(summary_df,
                                     archetype_col = "best_archetype",
                                     min_group_size = 5,
                                     top_n_groups = None,
                                     sort_by = "median_IDF",
                                     ascending = False,
                                     groups_to_keep = None):
    """
    Select archetype groups to include in the boxplot.
    """

    selected_summary_df = summary_df.copy()

    if groups_to_keep is not None:
        if isinstance(groups_to_keep, str):
            groups_to_keep = [groups_to_keep]

        selected_summary_df = selected_summary_df[
            selected_summary_df[archetype_col].isin(groups_to_keep)
        ]

    else:
        selected_summary_df = selected_summary_df[
            selected_summary_df["n_features"] >= min_group_size
        ]

        if sort_by is not None:
            selected_summary_df = selected_summary_df.sort_values(sort_by,
                                                                  ascending = ascending)

        if top_n_groups is not None:
            selected_summary_df = selected_summary_df.head(top_n_groups)

    selected_groups = selected_summary_df[archetype_col].tolist()

    return selected_groups, selected_summary_df
