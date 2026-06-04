from __future__ import annotations

from scipy.signal import savgol_filter

def smooth_savgol(context,
                  params):
    """
    Smooth a chromatogram with a Savitzky-Golay filter.

    Expected context keys:
        peak_chromatogram, min_window

    Relevant params:
        params["columns"]["int_col"]
        params["smoothing"]["savgol_min_poly"]
    """

    peak_chromatogram = context["peak_chromatogram"]
    min_window = context["min_window"]

    int_col = params["columns"]["int_col"]
    min_poly = params["smoothing"]["savgol_min_poly"]

    smooth_savgol_chromatogram = peak_chromatogram.copy()
    n_spectra = len(peak_chromatogram[:, int_col])
    window_length = min([int(n_spectra / 4) * 2 + 1,
                         min_window])

    poly_order = min([int(window_length / 3),
                      min_poly])

    soft_intensity = savgol_filter(peak_chromatogram[:, int_col],
                                   window_length,
                                   poly_order)

    smooth_savgol_chromatogram[:, int_col] = soft_intensity

    return smooth_savgol_chromatogram
