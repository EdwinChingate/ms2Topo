from __future__ import annotations

import pandas as pd
import numpy as np

def make_selected_feature_role_table(selected_feature_cols,
                                     group_feature_ids,
                                     molecule_feature_ids):
    """
    Annotate selected features according to their origin.
    """

    group_feature_ids = set(clean_id_series(group_feature_ids).tolist())
    molecule_feature_ids = set(clean_id_series(molecule_feature_ids).tolist())

    rows = []

    for feature_col in selected_feature_cols:

        feature_id = clean_id_value(feature_col)

        is_group_feature = feature_id in group_feature_ids
        is_molecule_feature = feature_id in molecule_feature_ids

        if is_group_feature and is_molecule_feature:
            feature_role = "group_and_molecule"

        elif is_group_feature:
            feature_role = "group_feature"

        elif is_molecule_feature:
            feature_role = "molecule_feature"

        else:
            feature_role = "unknown"

        rows.append({"feat_id": feature_col,
                     "feature_role": feature_role,
                     "is_group_feature": is_group_feature,
                     "is_molecule_feature": is_molecule_feature})

    feature_role_df = pd.DataFrame(rows)

    return feature_role_df
