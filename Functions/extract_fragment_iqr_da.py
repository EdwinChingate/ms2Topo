# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import numpy as np
import pandas as pd


def extract_fragment_iqr_da(consensus_spectrum_df,
                            mz_col = "median_mz(Da)",
                            mz_std_col = "IQR_mz(Da)",
                            mz_iqr_ppm_col = "IQR_mz(ppm)",
                            min_mz_col = "min_mz(Da)",
                            max_mz_col = "max_mz(Da)"):
    """
    Extract or approximate fragment m/z IQR in Da from a consensus spectrum.

    The preferred source is mz_std_col if present. If not, IQR_mz(ppm) is
    converted to Da. If neither exists, min/max m/z columns are used as a
    fallback interval width. If no uncertainty information exists, zeros are
    returned.
    """

    fragment_mz = pd.to_numeric(consensus_spectrum_df[mz_col],
                                errors = "coerce").to_numpy(dtype = float)

    if mz_std_col in consensus_spectrum_df.columns:
        fragment_iqr_da = pd.to_numeric(consensus_spectrum_df[mz_std_col],
                                        errors = "coerce").to_numpy(dtype = float)

    elif mz_iqr_ppm_col in consensus_spectrum_df.columns:
        fragment_iqr_ppm = pd.to_numeric(consensus_spectrum_df[mz_iqr_ppm_col],
                                         errors = "coerce").to_numpy(dtype = float)

        fragment_iqr_da = fragment_iqr_ppm / 1e6 * fragment_mz

    elif min_mz_col in consensus_spectrum_df.columns and max_mz_col in consensus_spectrum_df.columns:
        fragment_min_mz = pd.to_numeric(consensus_spectrum_df[min_mz_col],
                                        errors = "coerce").to_numpy(dtype = float)

        fragment_max_mz = pd.to_numeric(consensus_spectrum_df[max_mz_col],
                                        errors = "coerce").to_numpy(dtype = float)

        fragment_iqr_da = np.abs(fragment_max_mz -
                                 fragment_min_mz)

    else:
        fragment_iqr_da = np.zeros(len(consensus_spectrum_df),
                                   dtype = float)

    fragment_iqr_da = np.where(np.isfinite(fragment_iqr_da) & (fragment_iqr_da >= 0),
                               fragment_iqr_da,
                               0.0)

    return fragment_iqr_da
