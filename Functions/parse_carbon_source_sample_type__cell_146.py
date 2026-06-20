from __future__ import annotations

import pandas as pd
from filter_assignments_by_sample_types import *

def parse_carbon_source_sample_type(sample_type,
                                    separator = " | "):
    """
    Parse a sample-type label into source and carbon-source components.

    Example
    -------
    "InfluentClean | Aniline"
        original_sample_type = "InfluentClean"
        sample_source = "Influent"
        clean_status = "clean"
        carbon_source = "Aniline"
    """

    if separator not in sample_type:
        return None

    original_sample_type, carbon_source = sample_type.split(separator,
                                                            1)

    if original_sample_type.endswith("Clean"):
        sample_source = original_sample_type.replace("Clean",
                                                     "")
        clean_status = "clean"

    else:
        sample_source = original_sample_type
        clean_status = "experimental"

    parsed_sample_type = {"sample_type": sample_type,
                          "original_sample_type": original_sample_type,
                          "sample_source": sample_source,
                          "clean_status": clean_status,
                          "carbon_source": carbon_source}

    return parsed_sample_type
