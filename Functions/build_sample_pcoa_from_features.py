from __future__ import annotations

import numpy as np
from sklearn.metrics import pairwise_distances
import pandas as pd
from classical_pcoa import *
from get_sample_columns_from_metadata import *

# TODO: unresolved names: sample_column

def build_sample_pcoa_from_features(AlignedSamplesDF,
                                    SamplesInfDF,
                                    drop_empty_samples = True):
    """
    Build a sample-level Jaccard distance matrix and project samples into 2D.

    Rows of AlignedSamplesDF are features.
    Sample columns are detected from SamplesInfDF.index.
    Positive feature values are treated as presence.
    """

    SampleColumns = get_sample_columns_from_metadata(AlignedSamplesDF = AlignedSamplesDF,
                                                     SamplesInfDF = SamplesInfDF)

    if len(SampleColumns) == 0:
        raise ValueError("No sample columns from SamplesInfDF.index were found in AlignedSamplesDF.")

    SampleFeatureDF = AlignedSamplesDF[SampleColumns].copy()

    SampleFeatureMat = SampleFeatureDF.to_numpy()
    SampleFeatureMat = (SampleFeatureMat > 0).T.astype(bool)

    SampleNames = np.array([str(sample_column) for sample_column in SampleColumns],
                           dtype = str)

    if drop_empty_samples:
        non_empty_samples = np.sum(SampleFeatureMat,
                                   axis = 1) > 0

        SampleFeatureMat = SampleFeatureMat[non_empty_samples, :]
        SampleNames = SampleNames[non_empty_samples]

    jaccard_distance_matrix = pairwise_distances(SampleFeatureMat,
                                                 metric = "jaccard")

    coordinates, explained_fraction, eigenvalues = classical_pcoa(distance_matrix = jaccard_distance_matrix,
                                                                  n_components = 2)

    PCoADF = pd.DataFrame({
        "sample_name": SampleNames,
        "PCoA1": coordinates[:, 0],
        "PCoA2": coordinates[:, 1],
    })

    SamplesInfDF_copy = SamplesInfDF.copy()
    SamplesInfDF_copy.index = SamplesInfDF_copy.index.astype(str)

    PCoADF = PCoADF.merge(SamplesInfDF_copy,
                          left_on = "sample_name",
                          right_index = True,
                          how = "left")

    return PCoADF, jaccard_distance_matrix, SampleFeatureMat, explained_fraction, eigenvalues    