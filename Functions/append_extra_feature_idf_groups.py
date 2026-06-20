from __future__ import annotations

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import textwrap

def append_extra_feature_idf_groups(feature_idf_archetype_df,
                                    extra_group_dfs):
    """
    Append one or more extra feature-IDF groups to the archetype table.
    """

    if extra_group_dfs is None:
        return feature_idf_archetype_df

    if not isinstance(extra_group_dfs, list):
        extra_group_dfs = [extra_group_dfs]

    combined_df = feature_idf_archetype_df.copy()

    for extra_group_df in extra_group_dfs:
        combined_df = pd.concat([combined_df,
                                 extra_group_df],
                                axis = 0,
                                ignore_index = True)

    return combined_df
