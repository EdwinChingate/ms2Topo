from __future__ import annotations

import numpy as np

def close_neighbours_list(context,
                          params):
    """
    Build neighbour lists by absolute signal difference.

    Expected context keys:
        signal_vec

    Relevant params:
        params["signal_clustering"]["use_observed_min_signal"]
        params["signal_clustering"]["min_signal"]
    """

    signal_vec = context["signal_vec"]

    if params["signal_clustering"]["use_observed_min_signal"]:
        min_signal = np.min(signal_vec)
    else:
        min_signal = params["signal_clustering"]["min_signal"]

    neighbours_list = []
    n_signals = len(signal_vec)
    signals_set = set(np.arange(n_signals,
                                dtype = int))

    for signal_id in signals_set:
        signal = signal_vec[signal_id]
        difference_signal_vec = np.abs(signal_vec - signal)
        neighbours = np.where(difference_signal_vec < min_signal)[0]
        neighbours_list.append(neighbours)

    return [neighbours_list,
            signals_set]
