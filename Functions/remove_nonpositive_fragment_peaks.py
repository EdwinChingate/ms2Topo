from __future__ import annotations
def remove_nonpositive_fragment_peaks(fragment_peak_table):
    positive_intensity_filter = fragment_peak_table[:, 1] > 0
    filtered_fragment_peak_table = fragment_peak_table[positive_intensity_filter, :]
    return filtered_fragment_peak_table