from __future__ import annotations

import pandas as pd

def build_sample_design_table(features_df,
                              samples_df,
                              sample_id_col = 'Sample ID',
                              group_cols = ('Source', 'Primary carbon source'),
                              drop_no_spe = True):
    """
    Build a sample-design table matching feature-table columns to sample metadata.

    Assumes sample IDs are encoded as five-digit strings, with:
        second-to-last digit = reactor/block
        last digit           = day/campaign

    For *_noSPE samples, either exclude them or annotate them separately.
    """

    features_df = features_df.copy()
    samples_df = samples_df.copy()

    samples_df[sample_id_col] = samples_df[sample_id_col].astype(str)

    sample_cols = []
    sample_ids = []

    for col in features_df.columns:
        col_str = str(col)

        if drop_no_spe and col_str.endswith("_noSPE"):
            continue

        clean_id = col_str.replace("_noSPE", "")

        if clean_id in set(samples_df[sample_id_col]):
            sample_cols.append(col)
            sample_ids.append(clean_id)

    sample_design = pd.DataFrame({
        "sample_col": sample_cols,
        sample_id_col: sample_ids
    })

    sample_design = sample_design.merge(
        samples_df[[sample_id_col, *group_cols]],
        on=sample_id_col,
        how="left"
    )

    sample_design["sample_type"] = (
        sample_design[list(group_cols)]
        .astype(str)
        .agg(" | ".join, axis=1)
    )

    sample_design["sample_id_str"] = sample_design[sample_id_col].astype(str)

    sample_design["reactor"] = sample_design["sample_id_str"].str[-2]
    sample_design["day"] = sample_design["sample_id_str"].str[-1]

    sample_design["block_id"] = (
        sample_design["sample_type"]
        + " | reactor_" + sample_design["reactor"]
    )

    return sample_design
