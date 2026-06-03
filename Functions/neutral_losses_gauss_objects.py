from __future__ import annotations

from neutral_losses_edges import *
from neutral_losses_histogram import *
from neutral_losses_objects_table import *

def neutral_losses_gauss_objects(mz_vec,
                                 bins=5000,
                                 FractionSample=100,
                                 mz_tol_factor=1.5,
                                 stdDistance=3,
                                 min_support_count=2):
    """
    Full neutral-loss mz object workflow.

    mz_vec
        → histogram
        → mz_Edges
        → PeakFeatStats
        → IQR / ppm descriptors
        → NeutralLossObjectsDF
    """

    NeutralLossPeaks, mz_centers, bin_width = neutral_losses_histogram(
        mz_vec=mz_vec,
        bins=bins
    )

    edgesVecList, SomePeaks = neutral_losses_edges(
        NeutralLossPeaks=NeutralLossPeaks,
        bin_width=bin_width,
        FractionSample=FractionSample,
        mz_tol_factor=mz_tol_factor
    )

    NeutralLossObjectsDF = neutral_losses_objects_table(
        edgesVecList=edgesVecList,
        SomePeaks=SomePeaks,
        stdDistance=stdDistance,
        min_support_count=min_support_count
    )

    return NeutralLossObjectsDF, NeutralLossPeaks, edgesVecList, SomePeaks
