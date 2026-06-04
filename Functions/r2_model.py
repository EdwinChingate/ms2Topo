from __future__ import annotations

import numpy as np

def r2_model(context,
             params):
    """
    Compute R² between a raw signal and a model signal.

    Expected context keys:
        raw_signal, model_signal
    """

    raw_signal = context["raw_signal"]
    model_signal = context["model_signal"]

    signal_mean = np.mean(raw_signal)
    ss_total = np.sum((raw_signal - signal_mean) ** 2)
    ss_residual = np.sum((model_signal - raw_signal) ** 2)
    r2 = 1 - ss_residual / ss_total

    return r2
