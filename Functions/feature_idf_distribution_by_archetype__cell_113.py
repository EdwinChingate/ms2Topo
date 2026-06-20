from __future__ import annotations

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import textwrap

def feature_idf_distribution_by_archetype(feature_idf_archetype_df,
                                          archetype_col = "best_archetype",
                                          idf_col = "weighted_mean_fragment_IDF"):
    """
    Calculate distribution descriptors of feature-level IDF for each archetype.
    """

    grouped = feature_idf_archetype_df.groupby(archetype_col)[idf_col]

    summary_df = grouped.agg(n_features = "size",
                             mean_IDF = "mean",
                             std_IDF = "std",
                             median_IDF = "median",
                             min_IDF = "min",
                             max_IDF = "max").reset_index()

    Q1 = grouped.quantile(0.25).reset_index(name = "Q1_IDF")
    Q3 = grouped.quantile(0.75).reset_index(name = "Q3_IDF")

    summary_df = pd.merge(summary_df,
                          Q1,
                          on = archetype_col,
                          how = "left")

    summary_df = pd.merge(summary_df,
                          Q3,
                          on = archetype_col,
                          how = "left")

    summary_df["IQR_IDF"] = summary_df["Q3_IDF"] - summary_df["Q1_IDF"]

    return summary_df
