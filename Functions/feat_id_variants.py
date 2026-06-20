from __future__ import annotations

import pandas as pd

def feat_id_variants(feat_id,
                     node_prefix = 'feat_'):
    """
    Generate likely graph-node representations for one feat_id.

    This helps when G uses nodes like:
        3515
        "3515"
        "3515.0"
        "feat_3515"
    """

    if pd.isna(feat_id):
        return []

    variants = []

    variants.append(feat_id)
    variants.append(str(feat_id))

    try:
        feat_id_float = float(feat_id)

        if feat_id_float.is_integer():
            feat_id_int = int(feat_id_float)

            variants.extend([
                feat_id_int,
                str(feat_id_int),
                float(feat_id_int),
                f"{node_prefix}{feat_id_int}"
            ])

        variants.append(str(feat_id_float))

    except Exception:
        pass

    # Preserve order but remove duplicates
    unique_variants = []
    seen = set()

    for variant in variants:
        key = (type(variant), str(variant))

        if key not in seen:
            unique_variants.append(variant)
            seen.add(key)

    return unique_variants
