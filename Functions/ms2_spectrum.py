from __future__ import annotations
from centroid_profile_ms2_spectrum_if_needed import *
from compute_relative_fragment_intensity_percent import *
from extract_fragment_peak_table import *
import numpy as np
from remove_nonpositive_fragment_peaks import *
from sort_fragment_peak_table_by_intensity import *

def ms2_spectrum(spectral_signals,
                 min_peaks = 1):
    if spectral_signals.getMSLevel() != 2:
        return []

    centroided_ms2_spectrum = centroid_profile_ms2_spectrum_if_needed(spectral_signals = spectral_signals)

    fragment_peak_table = extract_fragment_peak_table(spectral_signals = centroided_ms2_spectrum)

    fragment_peak_table = remove_nonpositive_fragment_peaks(fragment_peak_table = fragment_peak_table)

    if len(fragment_peak_table) < min_peaks:
        return []

    fragment_peak_table = sort_fragment_peak_table_by_intensity(fragment_peak_table = fragment_peak_table,
                                                                descending = True)

    relative_fragment_intensity_percent = compute_relative_fragment_intensity_percent(fragment_peak_table = fragment_peak_table)

    formatted_fragment_peak_table = np.hstack((fragment_peak_table,
                                               relative_fragment_intensity_percent))

    return formatted_fragment_peak_table