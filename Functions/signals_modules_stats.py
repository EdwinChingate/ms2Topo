from __future__ import annotations

import numpy as np

def signals_modules_stats(context,
                          params):
    """
    Summarize signal values inside connected modules.

    Expected context keys:
        modules, signal_vec
    """

    modules = context["modules"]
    signal_vec = context["signal_vec"]

    modules_stats = []
    module_location = 0

    for module in modules:
        signals = signal_vec[module]

        signals_mean = np.mean(signals)
        signals_std = np.std(signals)
        signals_max = np.max(signals)
        signals_min = np.min(signals)
        n_signals = len(module)

        modules_stats.append([signals_mean,
                              signals_std,
                              signals_max,
                              signals_min,
                              n_signals,
                              int(module_location)])

        module_location += 1

    modules_stats = np.array(modules_stats)
    modules_stats = modules_stats[modules_stats[:, 2].argsort(), :]

    return modules_stats
