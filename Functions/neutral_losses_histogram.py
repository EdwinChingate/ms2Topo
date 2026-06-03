from __future__ import annotations

import numpy as np

def neutral_losses_histogram(mz_vec,
                             bins=5000):
    """
    Build the histogram representation of the neutral-loss mz vector.

    Output format:
        NeutralLossPeaks[:, 0] = neutral-loss mz bin center
        NeutralLossPeaks[:, 1] = count
    """

    counts, edges = np.histogram(mz_vec, bins=bins)
    mz_centers = (edges[:-1] + edges[1:]) / 2

    NeutralLossPeaks = np.zeros((len(mz_centers), 2))
    NeutralLossPeaks[:, 0] = mz_centers
    NeutralLossPeaks[:, 1] = counts

    NeutralLossPeaks = NeutralLossPeaks[NeutralLossPeaks[:, 1] > 0, :]
    NeutralLossPeaks = NeutralLossPeaks[NeutralLossPeaks[:, 0].argsort(), :]

    bin_width = np.median(np.diff(mz_centers))

    return NeutralLossPeaks, mz_centers, bin_width
