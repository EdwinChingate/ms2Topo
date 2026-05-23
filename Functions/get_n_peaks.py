from __future__ import annotations

def get_n_peaks(spectrum):
    mz_array, intensity_array = spectrum.get_peaks()
    return min(len(mz_array), len(intensity_array))