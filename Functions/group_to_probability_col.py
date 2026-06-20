from __future__ import annotations

import numpy as np
import pandas as pd

def group_to_probability_col(group,
                             group_col_prefix = "p__"):
    """
    Convert a group label into the corresponding probability column name.
    """

    if str(group).startswith(group_col_prefix):
        return group

    return group_col_prefix + str(group)
