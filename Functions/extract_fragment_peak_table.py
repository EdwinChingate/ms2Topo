from __future__ import annotations
import numpy as np

def extract_fragment_peak_table(spectral_signals):
    fragment_mz_array, fragment_intensity_array = spectral_signals.get_peaks()

    if len(fragment_mz_array) == 0:
        return np.empty((0, 2))

    fragment_peak_table = np.column_stack((fragment_mz_array,
                                           fragment_intensity_array)).astype(float)

    return fragment_peak_table