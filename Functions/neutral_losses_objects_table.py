from __future__ import annotations

import numpy as np
import pandas as pd
from PeakFeatStats import *
from weighted_quantile import *

def neutral_losses_objects_table(edgesVecList,
                                 SomePeaks,
                                 stdDistance=3,
                                 min_support_count=2):
    """
    Build a neutral-loss object table from mz_Edges output.

    Uses:
        PeakFeatStats() for mz mean and std.
        weighted_quantile() for Q25, median, Q75 and IQR.
    """

    rows = []

    for loss_id, edgesVec in enumerate(edgesVecList):

        low = int(edgesVec[0])
        high = int(edgesVec[1])

        Peak = SomePeaks[low:high, :]

        if len(Peak) == 0:
            continue

        mz_mean, mz_std = PeakFeatStats(
            edgesVec=edgesVec,
            Peaks=SomePeaks
        )

        support = np.sum(Peak[:, 1])
        max_count = np.max(Peak[:, 1])
        n_bins = len(Peak[:, 0])

        q25, q50, q75 = weighted_quantile(
            values=Peak[:, 0],
            weights=Peak[:, 1],
            quantiles=[0.25, 0.50, 0.75]
        )

        iqr = q75 - q25

        rows.append({
            "neutral_loss_id": loss_id,

            "neutral_loss_mz_(Da)": mz_mean,
            "neutral_loss_mz_std_(Da)": mz_std,
            "neutral_loss_mz_std_(ppm)": mz_std / mz_mean * 1e6,

            "Q25_mz_(Da)": q25,
            "median_mz_(Da)": q50,
            "Q75_mz_(Da)": q75,
            "IQR_mz_(Da)": iqr,
            "IQR_mz_(ppm)": iqr / mz_mean * 1e6,

            "loss_support_count": support,
            "max_bin_count": max_count,
            "N_bins": n_bins,

            "min_mz_(Da)": mz_mean - stdDistance * mz_std,
            "max_mz_(Da)": mz_mean + stdDistance * mz_std,

            "raw_min_mz_(Da)": np.min(Peak[:, 0]),
            "raw_max_mz_(Da)": np.max(Peak[:, 0]),
        })

    NeutralLossObjectsDF = pd.DataFrame(rows)

    if len(NeutralLossObjectsDF) == 0:
        return NeutralLossObjectsDF

    NeutralLossObjectsDF = NeutralLossObjectsDF[
        NeutralLossObjectsDF["loss_support_count"] >= min_support_count
    ]

    NeutralLossObjectsDF = NeutralLossObjectsDF.sort_values(
        "neutral_loss_mz_(Da)"
    )

    NeutralLossObjectsDF = NeutralLossObjectsDF.reset_index(drop=True)

    return NeutralLossObjectsDF
