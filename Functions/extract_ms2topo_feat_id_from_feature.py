from __future__ import annotations

import re

def extract_ms2topo_feat_id_from_feature(feature):
    """
    Try to recover the original ms2Topo feat_id from SIRIUS feature metadata.
    """

    text_parts = []

    for value in feature.values():
        if isinstance(value, (str, int, float)):
            text_parts.append(str(value))

    feature_text = " ".join(text_parts)

    patterns = [r"ms2Topo_feat_(\d+)",
                r"feat_(\d+)",
                r"FEATURE_ID[=:_-](\d+)"]

    for pattern in patterns:
        match = re.search(pattern, feature_text)

        if match is not None:
            return int(match.group(1))

    return None
