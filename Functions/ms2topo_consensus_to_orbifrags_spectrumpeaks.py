from __future__ import annotations

import numpy as np

def ms2topo_consensus_to_orbifrags_spectrumpeaks(consensus_df,
                                                 mz_col = "median_mz(Da)",
                                                 intensity_col = "median_Int",
                                                 n_col = "N_spectra",
                                                 iqr_ppm_col = "IQR_mz(ppm)",
                                                 min_ci_ppm = 10.0,
                                                 fallback_ci_ppm = 10.0,
                                                 max_ci_ppm = 30.0,
                                                 min_relative_intensity = 0.0,
                                                 top_n = None,
                                                 intensity_normalization = "sum",
                                                 sort_by_mz = True,
                                                 return_df = False):
    """
    Convert one ms2Topo consensus MS2 spectrum into the SpectrumPeaks format
    expected by the OrbiFragsNets annotation functions.

    Returned array columns:

        0 -> MeassuredMZ
        1 -> Std
        2 -> NumberofDataPoints
        3 -> ConfidenceIntervalDa
        4 -> ConfidenceInterval
        5 -> RelativeIntensity

    The spelling 'MeassuredMZ' is kept for compatibility with the original
    OrbiFragsNets output table.
    """

    required_cols = [mz_col,
                     intensity_col,
                     n_col]

    if iqr_ppm_col is not None:
        required_cols.append(iqr_ppm_col)

    missing_cols = [col for col in required_cols if col not in consensus_df.columns]

    if len(missing_cols) > 0:
        raise ValueError(f"The following columns were not found: {missing_cols}. "
                         f"Available columns are: {list(consensus_df.columns)}")

    results_df = consensus_df.copy()

    results_df["MeassuredMZ"] = results_df[mz_col].astype(float)
    results_df["SourceIntensity"] = results_df[intensity_col].astype(float)
    results_df["NumberofDataPoints"] = results_df[n_col].fillna(2).astype(float)

    results_df = results_df.dropna(subset = ["MeassuredMZ",
                                             "SourceIntensity"]).copy()

    results_df = results_df[results_df["SourceIntensity"] > 0].copy()

    if len(results_df) == 0:
        raise ValueError("No valid consensus fragments were found after removing "
                         "missing m/z values and non-positive intensities.")

    results_df["NumberofDataPoints"] = results_df["NumberofDataPoints"].clip(lower = 2)

    if iqr_ppm_col is None:
        results_df["ConsensusIQRppm"] = fallback_ci_ppm

    else:
        results_df["ConsensusIQRppm"] = results_df[iqr_ppm_col].fillna(fallback_ci_ppm).astype(float)

    results_df["ConfidenceInterval"] = results_df["ConsensusIQRppm"].copy()
    results_df["ConfidenceInterval"] = results_df["ConfidenceInterval"].clip(lower = min_ci_ppm)

    if max_ci_ppm is not None:
        results_df["ConfidenceInterval"] = results_df["ConfidenceInterval"].clip(upper = max_ci_ppm)

    results_df["ConfidenceIntervalDa"] = results_df["MeassuredMZ"] * \
                                         results_df["ConfidenceInterval"] / 1e6

    results_df["Std"] = results_df["ConfidenceIntervalDa"] / 1.349

    if intensity_normalization == "sum":
        intensity_reference = results_df["SourceIntensity"].sum()

    elif intensity_normalization == "base_peak":
        intensity_reference = results_df["SourceIntensity"].max()

    else:
        raise ValueError("intensity_normalization must be either 'sum' or 'base_peak'.")

    if intensity_reference <= 0:
        raise ValueError("The intensity reference is zero or negative. "
                         "Relative intensities cannot be calculated.")

    results_df["RelativeIntensity"] = results_df["SourceIntensity"] / \
                                      intensity_reference * 100

    if min_relative_intensity > 0:
        results_df = results_df[results_df["RelativeIntensity"] >=
                                min_relative_intensity].copy()

    if len(results_df) == 0:
        raise ValueError("No fragments remained after the relative-intensity filter.")

    if top_n is not None:
        results_df = results_df.sort_values("RelativeIntensity",
                                            ascending = False).head(top_n).copy()

    if sort_by_mz:
        results_df = results_df.sort_values("MeassuredMZ").reset_index(drop = True)

    else:
        results_df = results_df.reset_index(drop = True)

    spectrum_peaks = np.array(results_df[["MeassuredMZ",
                                          "Std",
                                          "NumberofDataPoints",
                                          "ConfidenceIntervalDa",
                                          "ConfidenceInterval",
                                          "RelativeIntensity"]])

    if return_df:
        preferred_first_cols = ["MeassuredMZ",
                                "Std",
                                "NumberofDataPoints",
                                "ConfidenceIntervalDa",
                                "ConfidenceInterval",
                                "RelativeIntensity",
                                "SourceIntensity",
                                "ConsensusIQRppm",
                                mz_col,
                                intensity_col,
                                n_col,
                                iqr_ppm_col]

        preferred_first_cols = [col for col in preferred_first_cols
                                if col in results_df.columns]

        remaining_cols = [col for col in results_df.columns
                          if col not in preferred_first_cols]

        results_df = results_df[preferred_first_cols + remaining_cols]

        return spectrum_peaks, results_df

    return spectrum_peaks
