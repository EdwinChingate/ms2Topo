from __future__ import annotations

import pandas as pd

def samples_attributes_filter(SamplesInfDF,
                              AttributeList,
                              attributeList):
    """
    Build a boolean sample filter from paired metadata attributes and values.

    Each entry in AttributeList is matched against the corresponding entry in
    attributeList. The returned filter selects samples matching all requested
    metadata conditions.
    """

    if len(AttributeList) != len(attributeList):
        raise ValueError("AttributeList and attributeList must have the same length.")

    Filter = pd.Series(True,
                       index = SamplesInfDF.index)

    for Attribute, attribute in zip(AttributeList,
                                    attributeList):
        Filt = SamplesInfDF[Attribute] == attribute
        Filter = Filter & Filt

    return Filter