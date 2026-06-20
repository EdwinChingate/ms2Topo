from __future__ import annotations

def filter_assignments_by_sample_types(assignments,
                                       sample_types,
                                       mode = 'inclusive',
                                       require = 'any',
                                       pattern_col_prefix = '',
                                       copy = True):
    """
    Filter an archetype-assignment table by assigned sample-type pattern.

    Parameters
    ----------
    assignments:
        DataFrame returned by assign_features_to_archetypes.

    sample_types:
        str or list of str.
        Sample type names to use for filtering.

    mode:
        "inclusive" or "exclusive".

        inclusive:
            keep features whose assigned archetype includes the selected
            sample type(s).

        exclusive:
            keep features whose assigned archetype excludes the selected
            sample type(s).

    require:
        "any" or "all".

        Only relevant for mode="inclusive".

        any:
            keep features appearing in at least one selected sample type.

        all:
            keep features appearing in every selected sample type.

    pattern_col_prefix:
        Prefix used when creating the archetype-pattern columns.
        Use "" if your columns are exactly the sample type names.

    copy:
        Whether to return a copy of the filtered table.

    Returns
    -------
    filtered_assignments:
        Filtered assignments DataFrame.
    """

    if isinstance(sample_types, str):
        sample_types = [sample_types]

    sample_types = list(sample_types)

    pattern_cols = [
        f"{pattern_col_prefix}{sample_type}"
        for sample_type in sample_types
    ]

    missing_cols = [
        col
        for col in pattern_cols
        if col not in assignments.columns
    ]

    if len(missing_cols) > 0:
        raise ValueError(
            "The following sample-type pattern columns were not found: "
            f"{missing_cols}"
        )

    pattern_matrix = assignments[pattern_cols].astype(int)

    if mode == "inclusive":

        if require == "any":
            mask = pattern_matrix.sum(axis=1) > 0

        elif require == "all":
            mask = pattern_matrix.sum(axis=1) == len(pattern_cols)

        else:
            raise ValueError("require must be 'any' or 'all'.")

    elif mode == "exclusive":

        mask = pattern_matrix.sum(axis=1) == 0

    else:
        raise ValueError("mode must be 'inclusive' or 'exclusive'.")

    filtered_assignments = assignments.loc[mask]

    if copy:
        filtered_assignments = filtered_assignments.copy()

    return filtered_assignments
