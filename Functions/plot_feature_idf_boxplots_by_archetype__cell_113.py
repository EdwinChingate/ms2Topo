from __future__ import annotations

import matplotlib.pyplot as plt
import textwrap
import numpy as np
import pandas as pd

def plot_feature_idf_boxplots_by_archetype(feature_idf_archetype_df,
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
                                           output_path = None):
    """
    Plot feature-level IDF distributions for archetype groups as vertical
    stacked boxplots.

    The archetype groups are shown on the y-axis and the IDF distribution on
    the x-axis.
    """

    summary_df = feature_idf_distribution_by_archetype(
        feature_idf_archetype_df = feature_idf_archetype_df,
        archetype_col = archetype_col,
        idf_col = idf_col
    )

    selected_groups, selected_summary_df = select_archetype_groups_for_plot(
        summary_df = summary_df,
        archetype_col = archetype_col,
        min_group_size = min_group_size,
        top_n_groups = top_n_groups,
        sort_by = sort_by,
        ascending = ascending,
        groups_to_keep = groups_to_keep
    )

    plot_df = feature_idf_archetype_df[
        feature_idf_archetype_df[archetype_col].isin(selected_groups)
    ].copy()

    ordered_groups = selected_summary_df[archetype_col].tolist()

    box_data = []
    yticklabels = []

    for group in ordered_groups:
        group_values = plot_df.loc[
            plot_df[archetype_col] == group,
            idf_col
        ].dropna().to_numpy()

        box_data.append(group_values)

        group_size = selected_summary_df.loc[
            selected_summary_df[archetype_col] == group,
            "n_features"
        ].iloc[0]

        if wrap_labels is not None:
            wrapped_group = "\n".join(textwrap.wrap(group,
                                                    width = wrap_labels))
        else:
            wrapped_group = group

        yticklabels.append(f"{wrapped_group}\n(n={group_size})")

    figsize_height = max(4,
                         len(ordered_groups) * figsize_height_per_group)

    fig, ax = plt.subplots(figsize = (figsize_width,
                                      figsize_height))

    ax.boxplot(box_data,
               vert = False,
               labels = yticklabels,
               showfliers = showfliers)

    ax.set_xlabel(idf_col)
    ax.set_ylabel("Feature archetype")
    ax.set_title("Feature-level IDF distribution by archetype")

    plt.tight_layout()

    if output_path is not None:
        plt.savefig(output_path,
                    dpi = 300,
                    bbox_inches = "tight")

    return summary_df, selected_summary_df, fig, ax
