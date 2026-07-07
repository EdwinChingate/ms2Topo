# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations


def calculate_target_iqr_da(median_mz,
                            target_component_iqr_da = 1e-3,
                            target_component_iqr_ppm = 3):
    """
    Calculate the target component IQR in Da from absolute and ppm tolerances.
    """

    median_mz = float(median_mz)

    target_iqr_da = max(float(target_component_iqr_da),
                        float(target_component_iqr_ppm) / 1e6 * median_mz)

    return target_iqr_da
