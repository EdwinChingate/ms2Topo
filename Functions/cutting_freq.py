from __future__ import annotations

import numpy as np
from low_signal_clustering import *

def cutting_freq(context,
                 params):
    """
    Estimate the Fourier frequency threshold for smoothing.

    Expected context keys:
        fft_signal, frequencies

    Relevant params:
        params["smoothing"]["freq_std_distance"]
        params["smoothing"]["min_signal_fraction"]
    """

    fft_signal = context["fft_signal"]
    frequencies = context["frequencies"]

    freq_std_distance = params["smoothing"]["freq_std_distance"]
    min_signal_fraction = params["smoothing"]["min_signal_fraction"]

    n_signals = len(fft_signal)

    noise_context = {"signal_vec": np.abs(fft_signal)}
    noise_threshold_vec = low_signal_clustering(context = noise_context,
                                                params = params)[0]

    noise_threshold = noise_threshold_vec[2]
    noise_location = fft_signal <= noise_threshold
    noise_frequency = frequencies[noise_location]

    frequency_mean = np.mean(abs(noise_frequency))
    frequency_std = np.std(abs(noise_frequency))
    frequency_threshold = frequency_mean - frequency_std * freq_std_distance

    min_signal_number = int(n_signals * min_signal_fraction)
    frequency_vec = np.abs(frequencies[np.abs(frequencies).argsort()].copy())
    min_frequency_threshold = frequency_vec[min_signal_number]

    frequency_threshold = np.max([frequency_threshold,
                                  min_frequency_threshold])

    return frequency_threshold
