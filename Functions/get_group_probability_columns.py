from __future__ import annotations

import numpy as np
import pandas as pd

def get_group_probability_columns(assignment_df,
                                  group_col_prefix = "p__"):
    """
    Get the sample-group probability/prevalence columns.
    """

    group_cols = [col for col in assignment_df.columns
                  if str(col).startswith(group_col_prefix)]

    return group_cols
