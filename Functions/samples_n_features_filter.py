from __future__ import annotations

import numpy as np
import pandas as pd
from samples_names_common_attributes import *

# TODO: unresolved names: column, sample_name

def samples_n_features_filter(AlignedSamplesDF,
                              SamplesInfDF,
                              AttributeList,
                              attributeList,
                              Min_Feat,
                              MoreThan = True):
    """
    Filter features by their occurrence count in samples matching metadata values.

    Positive values in the selected sample columns are treated as feature
    presence. The returned filter selects features appearing in at least
    Min_Feat samples when MoreThan is True, or fewer than Min_Feat samples when
    MoreThan is False.
    """

    SampleNames = samples_names_common_attributes(SamplesInfDF = SamplesInfDF,
                                                  AttributeList = AttributeList,
                                                  attributeList = attributeList)

    column_map = {str(column): column for column in AlignedSamplesDF.columns}

    SampleColumns = [column_map[sample_name] for sample_name in SampleNames
                     if sample_name in column_map]

    if len(SampleColumns) == 0:
        raise ValueError("No matching sample columns were found in AlignedSamplesDF.")

    SamplesDF = AlignedSamplesDF[SampleColumns].copy()

    SampLocMat = SamplesDF.to_numpy()
    SampLocMat = (SampLocMat > 0).astype(int)

    FeatureCountVec = np.sum(SampLocMat,
                             axis = 1)

    Filter = pd.Series(FeatureCountVec >= Min_Feat,
                       index = AlignedSamplesDF.index)

    if MoreThan:
        return [Filter,
                SampleColumns]

    return [~Filter,
            SampleColumns]