from __future__ import annotations

import pandas as pd
from filter_assignments_by_sample_types import *
from sample_type_table_from_assignments import sample_type_table_from_assignments

def select_sample_types_by_groups(assignments,
                                  carbon_sources = None,
                                  sample_sources = None,
                                  original_sample_types = None,
                                  clean_status = None,
                                  pattern_col_prefix = "",
                                  separator = " | "):
    """
    Select sample-type names from an archetype-assignment table based on
    carbon source and original sample type.

    Parameters
    ----------
    carbon_sources:
        str, list of str, or None.
        Examples: "Aniline", "Histidine", "Succinate".

    sample_sources:
        str, list of str, or None.
        Examples: "Influent", "Effluent".

    original_sample_types:
        str, list of str, or None.
        Examples: "Influent", "InfluentClean", "Effluent", "EffluentClean".

    clean_status:
        str, list of str, or None.
        Examples: "clean", "experimental".
    """

    sample_type_df = sample_type_table_from_assignments(assignments = assignments,
                                                        pattern_col_prefix = pattern_col_prefix,
                                                        separator = separator)

    if sample_type_df.empty:
        raise ValueError("No sample-type pattern columns were detected.")

    if isinstance(carbon_sources, str):
        carbon_sources = [carbon_sources]

    if isinstance(sample_sources, str):
        sample_sources = [sample_sources]

    if isinstance(original_sample_types, str):
        original_sample_types = [original_sample_types]

    if isinstance(clean_status, str):
        clean_status = [clean_status]

    selected_sample_type_df = sample_type_df.copy()

    if carbon_sources is not None:
        selected_sample_type_df = selected_sample_type_df[
            selected_sample_type_df["carbon_source"].isin(carbon_sources)
        ]

    if sample_sources is not None:
        selected_sample_type_df = selected_sample_type_df[
            selected_sample_type_df["sample_source"].isin(sample_sources)
        ]

    if original_sample_types is not None:
        selected_sample_type_df = selected_sample_type_df[
            selected_sample_type_df["original_sample_type"].isin(original_sample_types)
        ]

    if clean_status is not None:
        selected_sample_type_df = selected_sample_type_df[
            selected_sample_type_df["clean_status"].isin(clean_status)
        ]

    selected_sample_types = selected_sample_type_df["sample_type"].tolist()

    return selected_sample_types
