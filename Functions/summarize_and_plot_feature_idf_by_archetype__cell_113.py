from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import textwrap

def summarize_and_plot_feature_idf_by_archetype(feature_idf_df,
                                                assignments,
                                                feat_id_col = "feat_id",
                                                archetype_col = "best_archetype",
                                                idf_col = "weighted_mean_fragment_IDF",
                                                min_group_size = 5,
                                                top_n_groups = 30,
                                                sort_by = "median_IDF",
                                                ascending = False,
                                                groups_to_keep = None,
                                                wrap_labels = 50,
                                                figsize_width = 12,
                                                figsize_height_per_group = 0.45,
                                                showfliers = False,
                                                output_path = None,
                                                extra_group_dfs = None):
    """
    Merge feature-level IDF with archetype labels, optionally append extra
    custom groups, estimate distribution descriptors, and plot boxplots by
    group.
    """

    feature_idf_archetype_df = merge_feature_idf_with_archetypes(
        feature_idf_df = feature_idf_df,
        assignments = assignments,
        feat_id_col = feat_id_col,
        archetype_col = archetype_col,
        idf_col = idf_col
    )

    feature_idf_archetype_df = append_extra_feature_idf_groups(
        feature_idf_archetype_df = feature_idf_archetype_df,
        extra_group_dfs = extra_group_dfs
    )

    summary_df, selected_summary_df, fig, ax = plot_feature_idf_boxplots_by_archetype(
        feature_idf_archetype_df = feature_idf_archetype_df,
        archetype_col = archetype_col,
        idf_col = idf_col,
        min_group_size = min_group_size,
        top_n_groups = top_n_groups,
        sort_by = sort_by,
        ascending = ascending,
        groups_to_keep = groups_to_keep,
        wrap_labels = wrap_labels,
        figsize_width = figsize_width,
        figsize_height_per_group = figsize_height_per_group,
        showfliers = showfliers,
        output_path = output_path
    )

    return feature_idf_archetype_df, summary_df, selected_summary_df, fig, ax
