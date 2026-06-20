from __future__ import annotations

import numpy as np
import pandas as pd

def select_unique_fragments_for_group(experiment_fragments_df,
                                      group,
                                      fragment_id_col = "feat_id",
                                      presence_threshold = 0,
                                      absence_threshold = 0,
                                      group_col_prefix = "p__"):
    """
    Select aligned fragments unique to a sample-distribution group.
    """

    fragment_ids = ids_unique_to_group(assignment_df = experiment_fragments_df,
                                       group = group,
                                       id_col = fragment_id_col,
                                       presence_threshold = presence_threshold,
                                       absence_threshold = absence_threshold,
                                       group_col_prefix = group_col_prefix)

    return fragment_ids
