from __future__ import annotations

from mz_Edges import *

def neutral_losses_edges(NeutralLossPeaks,
                         bin_width,
                         FractionSample=100,
                         mz_tol_factor=1.5):
    """
    Group adjacent occupied neutral-loss mz bins using mz_Edges.
    """

    edgesVecList, SomePeaks = mz_Edges(
        AllRawPeaks=NeutralLossPeaks,
        FractionSample=FractionSample,
        mz_tol=bin_width * mz_tol_factor
    )

    return edgesVecList, SomePeaks
