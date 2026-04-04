from __future__ import annotations
import numpy as np

def compute_relative_fragment_intensity_percent(fragment_peak_table):
    if len(fragment_peak_table) == 0:
        return np.empty((0, 1))

    base_peak_intensity = fragment_peak_table[0, 1]

    relative_fragment_intensity_percent = (fragment_peak_table[:, 1] / base_peak_intensity * 100).reshape(-1, 1)

    return relative_fragment_intensity_percent