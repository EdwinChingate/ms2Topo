from __future__ import annotations

import numpy as np
from samples_attributes_filter import *

def samples_names_common_attributes(SamplesInfDF,
                                    AttributeList,
                                    attributeList):
    """
    Return sample names whose metadata match a list of attribute-value pairs.

    The function assumes that SamplesInfDF.index contains the sample names used
    as columns in the aligned feature table.
    """

    Filter = samples_attributes_filter(SamplesInfDF = SamplesInfDF,
                                       AttributeList = AttributeList,
                                       attributeList = attributeList)

    Index = SamplesInfDF[Filter].index
    Index = np.array(Index,
                     dtype = str)

    return Index