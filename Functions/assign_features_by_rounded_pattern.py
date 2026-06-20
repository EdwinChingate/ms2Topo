from __future__ import annotations

import numpy as np
import pandas as pd

def assign_features_by_rounded_pattern(P,
                                       feat_ids,
                                       group_names,
                                       threshold = 0.5,
                                       include_empty = False,
                                       empty_label = 'Absent',
                                       pattern_col_prefix = ''):
    """
    Assign features to exact binary sample-distribution patterns.

    P:
        n_features × n_groups probability matrix.

    feat_ids:
        feature identifiers.

    group_names:
        sample-type names matching the columns of P.

    threshold:
        probability threshold used to convert probabilities into 0/1.

        Example:
            threshold = 0.5 means probability >= 0.5 becomes 1.

    include_empty:
        If False, features rounded to all-zero are removed.

    Returns
    -------
    assignments:
        one row per feature, with its binary pattern and pattern label.

    pattern_summary:
        one row per repeated pattern, with the number of features assigned.
    """

    group_names = list(group_names)

    P = np.asarray(P,
                   dtype = float)

    binary_patterns = (P >= threshold).astype(int)

    pattern_cols = [
        pattern_col_prefix + group_name
        for group_name in group_names
    ]

    assignments = pd.DataFrame(binary_patterns,
                               columns = pattern_cols)

    assignments.insert(0,
                       "feat_id",
                       feat_ids)

    pattern_labels = []

    for row_id in assignments.index:

        active_groups = [
            group_names[group_id]
            for group_id in range(len(group_names))
            if binary_patterns[row_id, group_id] == 1
        ]

        if len(active_groups) == 0:
            pattern_label = empty_label
        else:
            pattern_label = " + ".join(active_groups)

        pattern_labels.append(pattern_label)

    assignments.insert(1,
                       "best_archetype",
                       pattern_labels)

    assignments["n_active_sample_types"] = binary_patterns.sum(axis = 1)

    if not include_empty:

        assignments = assignments.loc[
            assignments["n_active_sample_types"] > 0
        ].copy()

    pattern_summary = (
        assignments
        .groupby(["best_archetype", "n_active_sample_types"])
        .size()
        .reset_index(name = "n_features")
        .sort_values("n_features",
                     ascending = False)
        .reset_index(drop = True)
    )

    assignments = assignments.merge(pattern_summary[["best_archetype",
                                                     "n_features"]],
                                    on = "best_archetype",
                                    how = "left")

    assignments = assignments.rename(columns = {
        "n_features": "archetype_size"
    })

    return assignments, pattern_summary
