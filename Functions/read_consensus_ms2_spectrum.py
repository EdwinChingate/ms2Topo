from __future__ import annotations

from pathlib import Path
import pandas as pd
from clean_feat_id import *
from normalize_intensity_vector import *

def read_consensus_ms2_spectrum(consensus_spectrum_path,
                                feat_id,
                                spectrum_id,
                                mz_col = "median_mz(Da)",
                                intensity_col = "mean_Int",
                                mz_std_col = "IQR_mz(Da)",
                                mz_iqr_ppm_col = "IQR_mz(ppm)",
                                drop_nonpositive_intensity = True,
                                normalization = "l2"):
    """
    Read one saved ms2Topo consensus spectrum and prepare it for alignment.

    The original feat_id is kept in 'feat_id'.
    The dense alignment index is stored in 'spectrum_id'.

    If normalization = "l2", fragment intensities are normalized to unit vector
    norm, which makes dot products directly comparable as cosine similarities.
    """

    consensus_spectrum_path = Path(consensus_spectrum_path)

    consensus_spectrum_df = pd.read_csv(consensus_spectrum_path)

    unnamed_cols = [col for col in consensus_spectrum_df.columns
                    if str(col).startswith("Unnamed")]

    if len(unnamed_cols) > 0:
        consensus_spectrum_df = consensus_spectrum_df.drop(columns = unnamed_cols)

    required_cols = [mz_col,
                     intensity_col]

    for col in required_cols:
        if col not in consensus_spectrum_df.columns:
            raise ValueError(f"Column '{col}' was not found in {consensus_spectrum_path}. "
                             f"Available columns: {list(consensus_spectrum_df.columns)}")

    consensus_spectrum_df = consensus_spectrum_df.copy()

    consensus_spectrum_df[mz_col] = pd.to_numeric(consensus_spectrum_df[mz_col],
                                                  errors = "coerce")

    consensus_spectrum_df[intensity_col] = pd.to_numeric(consensus_spectrum_df[intensity_col],
                                                         errors = "coerce")

    consensus_spectrum_df = consensus_spectrum_df.dropna(subset = [mz_col,
                                                                   intensity_col])

    if drop_nonpositive_intensity:
        consensus_spectrum_df = consensus_spectrum_df[
            consensus_spectrum_df[intensity_col] > 0
        ].copy()

    if len(consensus_spectrum_df) == 0:
        return consensus_spectrum_df

    consensus_spectrum_df = normalize_intensity_vector(spectrum_df = consensus_spectrum_df,
                                                       intensity_col = intensity_col,
                                                       normalization = normalization)

    if mz_std_col not in consensus_spectrum_df.columns:
        if mz_iqr_ppm_col not in consensus_spectrum_df.columns:
            raise ValueError(f"Neither '{mz_std_col}' nor '{mz_iqr_ppm_col}' was found in "
                             f"{consensus_spectrum_path}.")

        consensus_spectrum_df[mz_iqr_ppm_col] = pd.to_numeric(consensus_spectrum_df[mz_iqr_ppm_col],
                                                              errors = "coerce")

        consensus_spectrum_df[mz_std_col] = (consensus_spectrum_df[mz_iqr_ppm_col] / 1e6 * consensus_spectrum_df[mz_col])

    consensus_spectrum_df[mz_std_col] = pd.to_numeric(consensus_spectrum_df[mz_std_col],
                                                      errors = "coerce")

    consensus_spectrum_df = consensus_spectrum_df.dropna(subset = [mz_std_col])

    consensus_spectrum_df["feat_id"] = clean_feat_id(feat_id)
    consensus_spectrum_df["spectrum_id"] = int(spectrum_id)
    consensus_spectrum_df["consensus_spectrum_file"] = str(consensus_spectrum_path)

    consensus_spectrum_df = consensus_spectrum_df.sort_values(mz_col).reset_index(drop = True)

    return consensus_spectrum_df