from __future__ import annotations

from scipy.signal import find_peaks
from smooth_fourier import *
from smooth_savgol import *

def smooth_data_and_find_peaks(context,
                               params):
    """
    Smooth a chromatogram and find local maxima.

    Expected context keys:
        chromatogram

    Relevant params:
        params["smoothing"]["min_poly"]
        params["smoothing"]["prominence"]
        params["smoothing"]["distance"]
    """

    chromatogram = context["chromatogram"]

    min_poly = params["smoothing"]["min_poly"]
    prominence = params["smoothing"]["prominence"]
    distance = params["smoothing"]["distance"]

    fourier_context = {"peak_chromatogram": chromatogram,
                       "suggest_savgol_window": True}

    smooth_fourier_chromatogram, savgol_window = smooth_fourier(context = fourier_context,
                                                                params = params)

    savgol_context = {"peak_chromatogram": smooth_fourier_chromatogram,
                      "min_window": savgol_window}

    local_params = params.copy()
    local_params["smoothing"] = params["smoothing"].copy()
    local_params["smoothing"]["savgol_min_poly"] = min_poly

    smooth_peaks = smooth_savgol(context = savgol_context,
                                 params = local_params)

    peaks_max = find_peaks(smooth_peaks[:, 1],
                           prominence = prominence,
                           distance = distance)[0]

    return [smooth_peaks,
            peaks_max]
