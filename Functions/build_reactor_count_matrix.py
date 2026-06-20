from __future__ import annotations

import pandas as pd

def build_reactor_count_matrix(features_df,
                               sample_design,
                               feat_id_col = 'feat_id',
                               min_days_present = None):
    """
    Convert sample-level binary presence/absence into reactor/block-level counts.

    If min_days_present is None:
        keep counts as 0/3, 1/3, 2/3, 3/3.

    If min_days_present is an integer:
        convert each reactor/block into one Bernoulli observation:
            1 if feature is present in at least min_days_present days
            0 otherwise

        Example:
            min_days_present=2 means a feature must appear in at least 2/3 days
            to count as present in that reactor.
    """

    sample_cols = sample_design["sample_col"].tolist()
    X = features_df[sample_cols].astype(int)

    block_tables = []

    for block_id, block_df in sample_design.groupby("block_id"):
        cols = block_df["sample_col"].tolist()

        x = X[cols].sum(axis=1)

        if min_days_present is None:
            m = len(cols)
            block_counts = x
            block_trials = m
        else:
            block_counts = (x >= min_days_present).astype(int)
            block_trials = 1

        sample_type = block_df["sample_type"].iloc[0]

        block_tables.append({
            "block_id": block_id,
            "sample_type": sample_type,
            "reactor": block_df["reactor"].iloc[0],
            "n_days": len(cols),
            "counts": block_counts,
            "trials": block_trials
        })

    counts_df = pd.DataFrame({
        feat_id_col: features_df[feat_id_col].values
    })

    block_metadata = []

    for block in block_tables:
        counts_df[block["block_id"]] = block["counts"].values

        block_metadata.append({
            "block_id": block["block_id"],
            "sample_type": block["sample_type"],
            "reactor": block["reactor"],
            "n_days": block["n_days"],
            "trials": block["trials"]
        })

    block_metadata = pd.DataFrame(block_metadata)

    counts = counts_df.drop(columns=[feat_id_col]).to_numpy(dtype=float)
    trials = block_metadata["trials"].to_numpy(dtype=float)

    group_names = block_metadata["sample_type"].drop_duplicates().tolist()
    group_to_idx = {group: i for i, group in enumerate(group_names)}

    group_idx = (
        block_metadata["sample_type"]
        .map(group_to_idx)
        .to_numpy(dtype=int)
    )

    feat_ids = counts_df[feat_id_col].to_numpy()

    return counts, trials, group_idx, group_names, feat_ids, block_metadata, counts_df
