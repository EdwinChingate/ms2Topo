from __future__ import annotations

# TODO: unresolved names: column

def get_sample_columns_from_metadata(AlignedSamplesDF,
                                     SamplesInfDF):
    """
    Find feature-table columns corresponding to sample names in SamplesInfDF.
    """

    column_map = {str(column): column for column in AlignedSamplesDF.columns}

    SampleColumns = []

    for sample_name in SamplesInfDF.index.astype(str):
        if sample_name in column_map:
            SampleColumns.append(column_map[sample_name])

    return SampleColumns