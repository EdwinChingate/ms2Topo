from __future__ import annotations

import numpy as np
from cutting_freq import *
from redistribute_sampling import *

def smooth_fourier(context,
                   params):
    """
    Smooth a chromatogram by removing high Fourier frequencies.

    Expected context keys:
        peak_chromatogram, suggest_savgol_window

    Relevant params:
        params["columns"]["rt_col"]
        params["columns"]["int_col"]
        params["smoothing"]["std_distance"]
        params["smoothing"]["savgol_window_times"]
        params["smoothing"]["max_signals"]
    """

    peak_chromatogram = context["peak_chromatogram"]
    suggest_savgol_window = context["suggest_savgol_window"]

    rt_col = params["columns"]["rt_col"]
    int_col = params["columns"]["int_col"]
    std_distance = params["smoothing"]["std_distance"]
    savgol_window_times = params["smoothing"]["savgol_window_times"]
    max_signals = params["smoothing"]["max_signals"]

    n_signals = len(peak_chromatogram[:, rt_col])

    redistribution_context = {"peak_chromatogram": peak_chromatogram,
                              "n_new": n_signals}

    redistributed_peak = redistribute_sampling(context = redistribution_context,
                                               params = params)

    time = redistributed_peak[:, 0]
    signal = redistributed_peak[:, 1]
    n_fft_signals = len(signal)

    min_rt = np.min(time)
    max_rt = np.max(time)
    rt_total = max_rt - min_rt
    sampling_rate = n_signals / rt_total

    fft_signal = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(n_fft_signals,
                                 d = (time[1] - time[0]))

    cutting_context = {"fft_signal": fft_signal,
                       "frequencies": frequencies}

    frequency_threshold = cutting_freq(context = cutting_context,
                                       params = params)

    fft_filtered = fft_signal.copy()
    fft_filtered[np.abs(frequencies) > frequency_threshold] = 0

    filtered_signal = np.fft.ifft(fft_filtered).real
    smooth_fourier_chromatogram = redistributed_peak.copy()
    smooth_fourier_chromatogram[:, 1] = np.abs(filtered_signal)

    n_signals = np.min([n_signals,
                        max_signals])

    redistribution_context = {"peak_chromatogram": smooth_fourier_chromatogram,
                              "n_new": n_signals}

    # redistributed_peak has rt/int columns at 0 and 1 after Fourier smoothing.
    local_params = params.copy()
    local_params["columns"] = params["columns"].copy()
    local_params["columns"]["rt_col"] = 0
    local_params["columns"]["int_col"] = 1

    smooth_fourier_chromatogram = redistribute_sampling(context = redistribution_context,
                                                        params = local_params)

    if suggest_savgol_window:
        savgol_window = sampling_rate / frequency_threshold * savgol_window_times
        savgol_window_odd = int(savgol_window / 2) * 2 + 1

        return [smooth_fourier_chromatogram,
                savgol_window_odd]

    return smooth_fourier_chromatogram
