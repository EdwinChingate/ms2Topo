from __future__ import annotations

from pyopenms import MSSpectrum
import numpy as np

def copy_spectrum_with_mz_filtered_peaks(spectrum,
                                          min_mz,
                                          max_mz):
    """
    Returns a copied MSSpectrum whose peak arrays are filtered by m/z.

    Metadata such as RT, MS level, native ID, precursors, and scan metadata
    are preserved by copying the original spectrum first.
    """

    filtered_spectrum = MSSpectrum(spectrum)

    mz_array, intensity_array = spectrum.get_peaks()

    mz_array = np.asarray(mz_array, dtype=float)
    intensity_array = np.asarray(intensity_array, dtype=float)

    if len(mz_array) == 0 or len(intensity_array) == 0:
        filtered_spectrum.set_peaks((np.array([], dtype=float),
                                     np.array([], dtype=float)))
        return filtered_spectrum

    n = min(len(mz_array), len(intensity_array))

    mz_array = mz_array[:n]
    intensity_array = intensity_array[:n]

    keep = (mz_array >= min_mz) & (mz_array <= max_mz)

    filtered_spectrum.set_peaks((mz_array[keep],
                                 intensity_array[keep]))

    return filtered_spectrum