from __future__ import annotations

from close_neighbours_list import *
from ms2_feat_modules import *
from signals_modules_stats import *

def low_signal_clustering(context,
                          params):
    """
    Identify the low-signal module used as noise threshold evidence.

    Expected context keys:
        signal_vec
    """

    signal_vec_0 = context["signal_vec"]

    zero_filter = signal_vec_0 > 0
    signal_vec = signal_vec_0[zero_filter]

    neighbours_context = {"signal_vec": signal_vec}

    neighbours_list, signals_set = close_neighbours_list(context = neighbours_context,
                                                         params = params)

    modules_context = {"adjacency_list": neighbours_list,
                       "node_ids": signals_set}

    modules = ms2_feat_modules(context = modules_context,
                               params = params)

    stats_context = {"modules": modules,
                     "signal_vec": signal_vec}

    modules_stats = signals_modules_stats(context = stats_context,
                                          params = params)

    noise_threshold_vec = modules_stats[0, :]
    module_location = int(noise_threshold_vec[-1])
    module = modules[module_location]
    noise_threshold_list = [noise_threshold_vec,
                            module]

    return noise_threshold_list
