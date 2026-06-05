from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from neutral_loss_normalize_intensity_vector import *

def read_consensus_spectrum_arrays(consensus_spectrum_path,
                                   mz_col = "median_mz(Da)",
                                   intensity_col = "median_Int",
                                   mz_std_col = "IQR_mz(Da)",
                                   mz_iqr_ppm_col = "IQR_mz(ppm)",
                                   drop_nonpositive_intensity = True,
                                   normalization = "l2"):
    """
    Read one consensus spectrum as sorted NumPy arrays.
    """

    consensus_spectrum_path = Path(consensus_spectrum_path)
    spectrum_df = pd.read_csv(consensus_spectrum_path)

    unnamed_cols = [col for col in spectrum_df.columns
                    if str(col).startswith("Unnamed")]

    if len(unnamed_cols) > 0:
        spectrum_df = spectrum_df.drop(columns = unnamed_cols)

    for col in [mz_col, intensity_col]:
        if col not in spectrum_df.columns:
            raise ValueError(f"Column '{col}' was not found in {consensus_spectrum_path}. "
                             f"Available columns: {list(spectrum_df.columns)}")

    mz_vec = pd.to_numeric(spectrum_df[mz_col],
                           errors = "coerce").to_numpy(dtype = float)

    intensity_vec = pd.to_numeric(spectrum_df[intensity_col],
                                  errors = "coerce").to_numpy(dtype = float)

    if mz_std_col in spectrum_df.columns:
        mz_std_vec = pd.to_numeric(spectrum_df[mz_std_col],
                                   errors = "coerce").to_numpy(dtype = float)

    elif mz_iqr_ppm_col in spectrum_df.columns:
        mz_iqr_ppm_vec = pd.to_numeric(spectrum_df[mz_iqr_ppm_col],
                                       errors = "coerce").to_numpy(dtype = float)

        mz_std_vec = mz_iqr_ppm_vec / 1e6 * mz_vec

    else:
        mz_std_vec = np.zeros(len(mz_vec),
                              dtype = float)

    original_fragment_id_vec = np.arange(len(mz_vec),
                                         dtype = int)

    good_fragments = (np.isfinite(mz_vec) &
                      np.isfinite(intensity_vec) &
                      np.isfinite(mz_std_vec))

    if drop_nonpositive_intensity:
        good_fragments = good_fragments & (intensity_vec > 0)

    mz_vec = mz_vec[good_fragments]
    intensity_vec = intensity_vec[good_fragments]
    mz_std_vec = mz_std_vec[good_fragments]
    original_fragment_id_vec = original_fragment_id_vec[good_fragments]

    if len(mz_vec) == 0:
        return {"fragment_mz": mz_vec,
                "fragment_intensity": intensity_vec,
                "fragment_mz_std": mz_std_vec,
                "fragment_id": original_fragment_id_vec}

    intensity_vec = neutral_loss_normalize_intensity_vector(intensity_vec = intensity_vec,
                                               normalization = normalization)

    order = np.argsort(mz_vec)

    return {"fragment_mz": mz_vec[order],
            "fragment_intensity": intensity_vec[order],
            "fragment_mz_std": mz_std_vec[order],
            "fragment_id": original_fragment_id_vec[order]}
