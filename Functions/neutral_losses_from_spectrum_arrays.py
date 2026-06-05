from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def neutral_losses_from_spectrum_arrays(fragment_mz,
                                        fragment_intensity,
                                        fragment_mz_std = None,
                                        fragment_id = None,
                                        min_neutral_loss = 18.0,
                                        max_neutral_loss = None,
                                        pair_intensity = "min"):
    """
    Calculate within-spectrum neutral-loss / fragment-difference arrays.

    The output is an array dictionary. No pandas objects are created here.
    """

    fragment_mz = np.asarray(fragment_mz,
                             dtype = float)

    fragment_intensity = np.asarray(fragment_intensity,
                                    dtype = float)

    n_fragments = len(fragment_mz)

    if fragment_mz_std is None:
        fragment_mz_std = np.zeros(n_fragments,
                                   dtype = float)

    else:
        fragment_mz_std = np.asarray(fragment_mz_std,
                                     dtype = float)

    if fragment_id is None:
        fragment_id = np.arange(n_fragments,
                                dtype = int)

    else:
        fragment_id = np.asarray(fragment_id,
                                 dtype = int)

    if n_fragments < 2:
        empty_float = np.array([], dtype = float)
        empty_int = np.array([], dtype = int)

        return {"neutral_loss_mz": empty_float,
                "neutral_loss_intensity": empty_float,
                "neutral_loss_mz_std": empty_float,
                "fragment_low_id": empty_int,
                "fragment_high_id": empty_int,
                "fragment_low_mz": empty_float,
                "fragment_high_mz": empty_float,
                "fragment_low_intensity": empty_float,
                "fragment_high_intensity": empty_float}

    loss_mz_chunks = []
    loss_intensity_chunks = []
    loss_mz_std_chunks = []
    low_id_chunks = []
    high_id_chunks = []
    low_mz_chunks = []
    high_mz_chunks = []
    low_intensity_chunks = []
    high_intensity_chunks = []

    for low_pos in range(n_fragments - 1):

        start_pos = np.searchsorted(fragment_mz,
                                    fragment_mz[low_pos] + min_neutral_loss,
                                    side = "left")

        if max_neutral_loss is None:
            stop_pos = n_fragments

        else:
            stop_pos = np.searchsorted(fragment_mz,
                                       fragment_mz[low_pos] + max_neutral_loss,
                                       side = "right")

        if start_pos >= stop_pos:
            continue

        high_pos = np.arange(start_pos,
                             stop_pos,
                             dtype = int)

        neutral_loss_mz = fragment_mz[high_pos] - fragment_mz[low_pos]

        low_intensity = np.repeat(fragment_intensity[low_pos],
                                  len(high_pos))

        high_intensity = fragment_intensity[high_pos]

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
            neutral_loss_intensity = np.ones(len(high_pos),
                                             dtype = float)

        else:
            raise ValueError("Unknown pair_intensity: " + str(pair_intensity))

        neutral_loss_mz_std = np.sqrt(fragment_mz_std[high_pos] ** 2 +
                                      fragment_mz_std[low_pos] ** 2)

        loss_mz_chunks.append(neutral_loss_mz)
        loss_intensity_chunks.append(neutral_loss_intensity)
        loss_mz_std_chunks.append(neutral_loss_mz_std)
        low_id_chunks.append(np.repeat(fragment_id[low_pos], len(high_pos)))
        high_id_chunks.append(fragment_id[high_pos])
        low_mz_chunks.append(np.repeat(fragment_mz[low_pos], len(high_pos)))
        high_mz_chunks.append(fragment_mz[high_pos])
        low_intensity_chunks.append(low_intensity)
        high_intensity_chunks.append(high_intensity)

    if len(loss_mz_chunks) == 0:
        empty_float = np.array([], dtype = float)
        empty_int = np.array([], dtype = int)

        return {"neutral_loss_mz": empty_float,
                "neutral_loss_intensity": empty_float,
                "neutral_loss_mz_std": empty_float,
                "fragment_low_id": empty_int,
                "fragment_high_id": empty_int,
                "fragment_low_mz": empty_float,
                "fragment_high_mz": empty_float,
                "fragment_low_intensity": empty_float,
                "fragment_high_intensity": empty_float}

    return {"neutral_loss_mz": np.concatenate(loss_mz_chunks),
            "neutral_loss_intensity": np.concatenate(loss_intensity_chunks),
            "neutral_loss_mz_std": np.concatenate(loss_mz_std_chunks),
            "fragment_low_id": np.concatenate(low_id_chunks),
            "fragment_high_id": np.concatenate(high_id_chunks),
            "fragment_low_mz": np.concatenate(low_mz_chunks),
            "fragment_high_mz": np.concatenate(high_mz_chunks),
            "fragment_low_intensity": np.concatenate(low_intensity_chunks),
            "fragment_high_intensity": np.concatenate(high_intensity_chunks)}
