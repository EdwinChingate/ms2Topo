from __future__ import annotations

from get_sample_columns_from_metadata import *

# TODO: unresolved names: column

def get_feature_metadata_columns(AlignedSamplesDF,
                                 SamplesInfDF):
    """
    Return all feature-table columns that are not sample columns.

    These columns are treated as feature descriptors and are preserved in the
    filtered output table.
    """

    SampleColumns = get_sample_columns_from_metadata(AlignedSamplesDF = AlignedSamplesDF,
                                                     SamplesInfDF = SamplesInfDF)

    FeatureMetadataColumns = [column for column in AlignedSamplesDF.columns
                              if column not in SampleColumns]

    return FeatureMetadataColumns