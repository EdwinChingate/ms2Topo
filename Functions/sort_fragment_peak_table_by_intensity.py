from __future__ import annotations
def sort_fragment_peak_table_by_intensity(fragment_peak_table,
                                          descending = True):
    if descending:
        sorted_fragment_peak_table = fragment_peak_table[(-fragment_peak_table[:, 1]).argsort(), :]
    else:
        sorted_fragment_peak_table = fragment_peak_table[fragment_peak_table[:, 1].argsort(), :]

    return sorted_fragment_peak_table