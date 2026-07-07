# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import numpy as np


def calculate_neutral_loss_iqr(low_iqr_da,
                               high_iqr_da,
                               neutral_loss_iqr_rule = "max_fragment_iqr"):
    """
    Estimate neutral-loss m/z uncertainty from the two fragments involved in
    the mass difference.

    neutral_loss_iqr_rule options:
        "max_fragment_iqr" -> max(low_iqr_da, high_iqr_da)
        "quadrature"       -> sqrt(low_iqr_da ** 2 + high_iqr_da ** 2)
    """

    if neutral_loss_iqr_rule not in ["max_fragment_iqr",
                                     "quadrature"]:
        raise ValueError("neutral_loss_iqr_rule must be 'max_fragment_iqr' or 'quadrature'.")

    low_iqr_da = np.asarray(low_iqr_da,
                            dtype = float)

    high_iqr_da = np.asarray(high_iqr_da,
                             dtype = float)

    low_iqr_da = np.where(np.isfinite(low_iqr_da) & (low_iqr_da >= 0),
                          low_iqr_da,
                          0.0)

    high_iqr_da = np.where(np.isfinite(high_iqr_da) & (high_iqr_da >= 0),
                           high_iqr_da,
                           0.0)

    if neutral_loss_iqr_rule == "max_fragment_iqr":
        neutral_loss_iqr_da = np.maximum(low_iqr_da,
                                         high_iqr_da)

    else:
        neutral_loss_iqr_da = np.sqrt(low_iqr_da ** 2 +
                                      high_iqr_da ** 2)

    return neutral_loss_iqr_da
