from __future__ import annotations

import numpy as np

def extract_mz_vec_by_neutral_loss_object(mz_vec,
                                          NeutralLossObject,
                                          min_col="min_mz_(Da)",
                                          max_col="max_mz_(Da)"):

    mz_vec = np.asarray(mz_vec, dtype=float)
    mz_vec = mz_vec[np.isfinite(mz_vec)]

    mz_min = NeutralLossObject[min_col]
    mz_max = NeutralLossObject[max_col]

    ObjectMzVec = mz_vec[
        (mz_vec >= mz_min) &
        (mz_vec <= mz_max)]

    return ObjectMzVec
