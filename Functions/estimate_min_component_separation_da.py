# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations


def estimate_min_component_separation_da(median_mz,
                                         min_component_separation_da = 1e-3,
                                         max_components_per_da = None,
                                         min_component_separation_ppm = 3):
    """
    Estimate the minimum allowed separation between two GMM component means.

    This implements a component-density constraint along the m/z axis, not a
    Gaussian probability-density overlap constraint.

    You can express the same idea as either:
        min_component_separation_da
            Minimum distance in Da between neighboring component means.

        max_components_per_da
            Maximum component density per Da. This is converted to:
                1 / max_components_per_da

    If several constraints are provided, the largest separation is used. This
    makes the rule conservative.
    """

    median_mz = float(median_mz)

    separation_candidates = []

    if min_component_separation_da is not None:

        min_component_separation_da = float(min_component_separation_da)

        if min_component_separation_da < 0:
            raise ValueError("min_component_separation_da must be >= 0.")

        separation_candidates.append(min_component_separation_da)

    if max_components_per_da is not None:

        max_components_per_da = float(max_components_per_da)

        if max_components_per_da <= 0:
            raise ValueError("max_components_per_da must be > 0.")

        separation_candidates.append(1.0 / max_components_per_da)

    if min_component_separation_ppm is not None:

        min_component_separation_ppm = float(min_component_separation_ppm)

        if min_component_separation_ppm < 0:
            raise ValueError("min_component_separation_ppm must be >= 0.")

        separation_candidates.append(min_component_separation_ppm / 1e6 * median_mz)

    if len(separation_candidates) == 0:
        raise ValueError("Provide at least one component-separation constraint.")

    minimum_separation_da = max(separation_candidates)

    return minimum_separation_da
