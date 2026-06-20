from __future__ import annotations

import pandas as pd

def normalize_archetype(archetype):
    if pd.isna(archetype):
        return ""

    return str(archetype).replace(" ", "").strip()
