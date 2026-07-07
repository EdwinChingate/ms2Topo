# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from clean_feat_id import clean_feat_id
from calculate_neutral_loss_iqr import calculate_neutral_loss_iqr
from extract_fragment_iqr_da import extract_fragment_iqr_da


def read_consensus_neutral_losses_spectrum(consensus_spectrum_path,
                                           feat_id,
                                           spectrum_id,
                                           mz_col = "median_mz(Da)",
                                           intensity_col = "median_Int",
                                           mz_std_col = "IQR_mz(Da)",
                                           mz_iqr_ppm_col = "IQR_mz(ppm)",
                                           min_mz_col = "min_mz(Da)",
                                           max_mz_col = "max_mz(Da)",
                                           min_source_fragment_intensity = 0.0,
                                           min_neutral_loss = 18.0,
                                           max_neutral_loss = None,
                                           neutral_loss_iqr_rule = "max_fragment_iqr",
                                           neutral_loss_presence_value = 1.0):
    """
    Read one consensus MS2 spectrum and generate neutral-loss observations.

    The returned table has the same minimum structural columns needed by the
    centroid-assignment pathway, but each row is a generated neutral loss
    instead of a directly observed fragment.

    Important columns for downstream assignment:
        neutral_loss_mz
        neutral_loss_iqr_da
        neutral_loss_presence
        fragment_id_in_spectrum
        feat_id
        spectrum_id
        consensus_spectrum_file

    Compatibility columns are also added:
        median_mz(Da)  = neutral_loss_mz
        IQR_mz(Da)    = neutral_loss_iqr_da
        IQR_mz(ppm)   = neutral_loss_iqr_ppm
        median_Int    = neutral_loss_presence
        fragment_mz   = neutral_loss_mz
        fragment_intensity = neutral_loss_presence
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

    n_raw_fragment_rows = int(len(consensus_spectrum_df))

    fragment_mz = pd.to_numeric(consensus_spectrum_df[mz_col],
                                errors = "coerce").to_numpy(dtype = float)

    fragment_intensity = pd.to_numeric(consensus_spectrum_df[intensity_col],
                                       errors = "coerce").to_numpy(dtype = float)

    fragment_iqr_da = extract_fragment_iqr_da(consensus_spectrum_df = consensus_spectrum_df,
                                              mz_col = mz_col,
                                              mz_std_col = mz_std_col,
                                              mz_iqr_ppm_col = mz_iqr_ppm_col,
                                              min_mz_col = min_mz_col,
                                              max_mz_col = max_mz_col)

    fragment_ids = np.arange(len(consensus_spectrum_df),
                             dtype = int)

    mz_is_valid = np.isfinite(fragment_mz)
    intensity_is_valid = np.isfinite(fragment_intensity)
    numeric_filter = mz_is_valid & intensity_is_valid

    n_missing_mz_fragments = int((~mz_is_valid).sum())
    n_missing_intensity_fragments = int((~intensity_is_valid).sum())
    n_fragments_after_numeric_filter = int(numeric_filter.sum())

    source_fragment_filter = (numeric_filter &
                              (fragment_intensity > min_source_fragment_intensity))

    n_fragments_filtered_by_intensity = int((numeric_filter & ~source_fragment_filter).sum())
    n_source_fragments_for_neutral_losses = int(source_fragment_filter.sum())

    filter_stats = {"feat_id": clean_feat_id(feat_id),
                    "spectrum_id": int(spectrum_id),
                    "n_raw_fragment_rows": n_raw_fragment_rows,
                    "n_missing_mz_fragments": n_missing_mz_fragments,
                    "n_missing_intensity_fragments": n_missing_intensity_fragments,
                    "n_fragments_after_numeric_filter": n_fragments_after_numeric_filter,
                    "min_source_fragment_intensity": float(min_source_fragment_intensity),
                    "n_fragments_filtered_by_intensity": n_fragments_filtered_by_intensity,
                    "n_source_fragments_for_neutral_losses": n_source_fragments_for_neutral_losses,
                    "n_generated_neutral_losses": 0}

    if n_source_fragments_for_neutral_losses < 2:
        neutral_losses_df = pd.DataFrame()
        neutral_losses_df.attrs["filter_stats"] = filter_stats
        return neutral_losses_df

    fragment_mz = fragment_mz[source_fragment_filter]
    fragment_intensity = fragment_intensity[source_fragment_filter]
    fragment_iqr_da = fragment_iqr_da[source_fragment_filter]
    fragment_ids = fragment_ids[source_fragment_filter]

    order = np.argsort(fragment_mz)

    fragment_mz = fragment_mz[order]
    fragment_intensity = fragment_intensity[order]
    fragment_iqr_da = fragment_iqr_da[order]
    fragment_ids = fragment_ids[order]

    n_fragments = len(fragment_mz)

    neutral_loss_tables = []
    neutral_loss_id = 0

    for low_id in range(n_fragments - 1):

        start_id = np.searchsorted(fragment_mz,
                                   fragment_mz[low_id] + min_neutral_loss,
                                   side = "left")

        if max_neutral_loss is None:
            stop_id = n_fragments

        else:
            stop_id = np.searchsorted(fragment_mz,
                                      fragment_mz[low_id] + max_neutral_loss,
                                      side = "right")

        if start_id >= stop_id:
            continue

        high_ids = np.arange(start_id,
                             stop_id,
                             dtype = int)

        neutral_loss_mz = fragment_mz[high_ids] - fragment_mz[low_id]

        low_iqr_da = np.repeat(fragment_iqr_da[low_id],
                               len(high_ids))

        high_iqr_da = fragment_iqr_da[high_ids]

        neutral_loss_iqr_da = calculate_neutral_loss_iqr(low_iqr_da = low_iqr_da,
                                                         high_iqr_da = high_iqr_da,
                                                         neutral_loss_iqr_rule = neutral_loss_iqr_rule)

        neutral_loss_iqr_ppm = np.where(neutral_loss_mz != 0,
                                        neutral_loss_iqr_da / neutral_loss_mz * 1e6,
                                        np.nan)

        neutral_loss_min_mz = neutral_loss_mz - 0.5 * neutral_loss_iqr_da
        neutral_loss_max_mz = neutral_loss_mz + 0.5 * neutral_loss_iqr_da

        low_intensity = np.repeat(fragment_intensity[low_id],
                                  len(high_ids))

        high_intensity = fragment_intensity[high_ids]

        current_n_losses = len(high_ids)
        current_presence = np.full(current_n_losses,
                                   float(neutral_loss_presence_value),
                                   dtype = float)

        current_loss_df = pd.DataFrame({"spectrum_id": np.repeat(int(spectrum_id),
                                                                  current_n_losses),
                                        "feat_id": np.repeat(clean_feat_id(feat_id),
                                                              current_n_losses),
                                        "feature_id": np.repeat(clean_feat_id(feat_id),
                                                                 current_n_losses),
                                        "source_file": np.repeat(consensus_spectrum_path.name,
                                                                 current_n_losses),
                                        "consensus_spectrum_file": np.repeat(str(consensus_spectrum_path),
                                                                             current_n_losses),
                                        "object_type": np.repeat("neutral_loss",
                                                                 current_n_losses),
                                        "neutral_loss_id_in_spectrum": np.arange(neutral_loss_id,
                                                                                 neutral_loss_id + current_n_losses,
                                                                                 dtype = int),
                                        "fragment_id_in_spectrum": np.arange(neutral_loss_id,
                                                                             neutral_loss_id + current_n_losses,
                                                                             dtype = int),
                                        "neutral_loss_mz": neutral_loss_mz,
                                        "neutral_loss_iqr_da": neutral_loss_iqr_da,
                                        "neutral_loss_iqr_ppm": neutral_loss_iqr_ppm,
                                        "neutral_loss_min_mz": neutral_loss_min_mz,
                                        "neutral_loss_max_mz": neutral_loss_max_mz,
                                        "neutral_loss_presence": current_presence,
                                        "raw_neutral_loss_presence": current_presence,
                                        mz_col: neutral_loss_mz,
                                        mz_std_col: neutral_loss_iqr_da,
                                        mz_iqr_ppm_col: neutral_loss_iqr_ppm,
                                        min_mz_col: neutral_loss_min_mz,
                                        max_mz_col: neutral_loss_max_mz,
                                        intensity_col: current_presence,
                                        "fragment_mz": neutral_loss_mz,
                                        "fragment_intensity": current_presence,
                                        "raw_fragment_intensity": current_presence,
                                        "fragment_low_id": np.repeat(fragment_ids[low_id],
                                                                     current_n_losses),
                                        "fragment_high_id": fragment_ids[high_ids],
                                        "fragment_low_mz": np.repeat(fragment_mz[low_id],
                                                                     current_n_losses),
                                        "fragment_high_mz": fragment_mz[high_ids],
                                        "fragment_low_intensity": low_intensity,
                                        "fragment_high_intensity": high_intensity,
                                        "fragment_low_iqr_da": low_iqr_da,
                                        "fragment_high_iqr_da": high_iqr_da})

        neutral_loss_tables.append(current_loss_df)
        neutral_loss_id += current_n_losses

    if len(neutral_loss_tables) == 0:
        neutral_losses_df = pd.DataFrame()

    else:
        neutral_losses_df = pd.concat(neutral_loss_tables,
                                      ignore_index = True)

        neutral_losses_df = neutral_losses_df.sort_values("neutral_loss_mz").reset_index(drop = True)

    filter_stats["n_generated_neutral_losses"] = int(len(neutral_losses_df))
    neutral_losses_df.attrs["filter_stats"] = filter_stats

    return neutral_losses_df
