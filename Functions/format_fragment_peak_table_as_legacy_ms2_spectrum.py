from __future__ import annotations
import numpy as np

def format_fragment_peak_table_as_legacy_ms2_spectrum(fragment_peak_table,
                                                      mz_std = 5e-4):
    if len(fragment_peak_table) == 0:
        return []

    if len(fragment_peak_table.shape) != 2:
        return []

    if fragment_peak_table.shape[1] == 10:
        return fragment_peak_table

    if fragment_peak_table.shape[1] == 2:
        relative_intensity_percent = (fragment_peak_table[:, 1] / np.max(fragment_peak_table[:, 1]) * 100).reshape(-1, 1)

        fragment_peak_table = np.hstack((fragment_peak_table,
                                         relative_intensity_percent))

    if fragment_peak_table.shape[1] != 3:
        return []

    number_of_peaks = len(fragment_peak_table[:, 0])

    fragment_mz_da = fragment_peak_table[:, 0].reshape(-1, 1)
    fragment_intensity = fragment_peak_table[:, 1].reshape(-1, 1)
    relative_intensity_percent = fragment_peak_table[:, 2].reshape(-1, 1)

    mz_std_da = np.ones((number_of_peaks, 1)) * mz_std
    gauss_r2 = np.zeros((number_of_peaks, 1))
    number_of_signals = np.ones((number_of_peaks, 1))
    confidence_interval_da = np.zeros((number_of_peaks, 1))
    confidence_interval_ppm = np.zeros((number_of_peaks, 1))
    mz_min_da = fragment_mz_da.copy()
    mz_max_da = fragment_mz_da.copy()

    legacy_ms2_spectrum = np.hstack((fragment_mz_da,
                                     mz_std_da,
                                     fragment_intensity,
                                     gauss_r2,
                                     number_of_signals,
                                     confidence_interval_da,
                                     confidence_interval_ppm,
                                     mz_min_da,
                                     mz_max_da,
                                     relative_intensity_percent))

    return legacy_ms2_spectrum