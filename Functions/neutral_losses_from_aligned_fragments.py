from __future__ import annotations

import numpy as np
import pandas as pd

def neutral_losses_from_aligned_fragments(aligned_intensity_df,
                                          aligned_mz_df = None,
                                          feature_cols = None,
                                          aligned_fragment_mz_col = "aligned_fragment_mz",
                                          min_neutral_loss = 18.0,
                                          max_neutral_loss = None,
                                          min_fragment_intensity = 0,
                                          pair_intensity = "min"):

    if feature_cols is None:
        feature_cols = [col for col in aligned_intensity_df.columns
                        if col != aligned_fragment_mz_col]

    aligned_fragment_mz_vec = aligned_intensity_df[aligned_fragment_mz_col].to_numpy(float)
    aligned_fragment_id_vec = np.arange(len(aligned_intensity_df),
                                        dtype = int)

    neutral_loss_tables = []
    feature_id_map_rows = []

    for spectrum_id, feature_col in enumerate(feature_cols):
        feature_id_map_rows.append({"spectrum_id": int(spectrum_id),
                                    "feature_col": feature_col})

        intensity_vec = aligned_intensity_df[feature_col].to_numpy(float)
        fragments_loc = intensity_vec > min_fragment_intensity

        if np.sum(fragments_loc) < 2:
            continue

        fragment_ids = aligned_fragment_id_vec[fragments_loc]
        fragment_intensity = intensity_vec[fragments_loc]

        if aligned_mz_df is None:
            fragment_mz = aligned_fragment_mz_vec[fragments_loc]
        else:
            fragment_mz = aligned_mz_df[feature_col].to_numpy(float)[fragments_loc]
            fallback_mz = aligned_fragment_mz_vec[fragments_loc]
            fragment_mz = np.where(fragment_mz > 0,
                                   fragment_mz,
                                   fallback_mz)

        order = np.argsort(fragment_mz)

        fragment_mz = fragment_mz[order]
        fragment_ids = fragment_ids[order]
        fragment_intensity = fragment_intensity[order]

        n_fragments = len(fragment_mz)

        loss_tables_current_spectrum = []

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

            low_intensity = np.repeat(fragment_intensity[low_id],
                                      len(high_ids))

            high_intensity = fragment_intensity[high_ids]

            if pair_intensity == "min":
                neutral_loss_intensity = np.minimum(low_intensity,
                                                    high_intensity)

            elif pair_intensity == "geometric_mean":
                neutral_loss_intensity = np.sqrt(low_intensity * high_intensity)

            elif pair_intensity == "mean":
                neutral_loss_intensity = 0.5 * (low_intensity + high_intensity)

            elif pair_intensity == "product":
                neutral_loss_intensity = low_intensity * high_intensity

            elif pair_intensity == "binary":
                neutral_loss_intensity = np.ones(len(high_ids),
                                                 dtype = float)

            else:
                raise ValueError("Unknown pair_intensity: " + str(pair_intensity))

            loss_tables_current_spectrum.append(pd.DataFrame({"spectrum_id": int(spectrum_id),
                                                              "feature_col": feature_col,
                                                              "neutral_loss_mz": neutral_loss_mz,
                                                              "neutral_loss_intensity": neutral_loss_intensity,
                                                              "fragment_low_id": fragment_ids[low_id],
                                                              "fragment_high_id": fragment_ids[high_ids],
                                                              "fragment_low_mz": fragment_mz[low_id],
                                                              "fragment_high_mz": fragment_mz[high_ids],
                                                              "fragment_low_intensity": low_intensity,
                                                              "fragment_high_intensity": high_intensity}))

        if len(loss_tables_current_spectrum) > 0:
            neutral_loss_tables.append(pd.concat(loss_tables_current_spectrum,
                                                 ignore_index = True))

    feature_id_map_df = pd.DataFrame(feature_id_map_rows)

    if len(neutral_loss_tables) == 0:
        neutral_losses_df = pd.DataFrame()
    else:
        neutral_losses_df = pd.concat(neutral_loss_tables,
                                      ignore_index = True)

    return {"neutral_losses_df": neutral_losses_df,
            "feature_id_map_df": feature_id_map_df}
