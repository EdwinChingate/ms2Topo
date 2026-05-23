from __future__ import annotations

from clean_feat_id import *

def get_feat_ids_from_features_table(features_table_df,
                                     feat_id_col = "feat_id"):
    """
    Extract feature IDs from an ms2Topo features table.
    """

    if feat_id_col not in features_table_df.columns:
        raise ValueError(f"feat_id_col='{feat_id_col}' was not found. "
                         f"Available columns: {list(features_table_df.columns)}")

    feat_ids = (features_table_df[feat_id_col]
                .apply(clean_feat_id)
                .dropna()
                .unique()
                .tolist())

    return feat_ids