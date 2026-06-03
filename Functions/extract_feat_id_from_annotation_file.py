from __future__ import annotations

import re
import os

def extract_feat_id_from_annotation_file(annotation_file,
                                         feat_id_pattern = r"feat[_-]?(\d+)|^(\d+)\.csv"):
    """
    Extract ms2Topo feat_id from an annotation file name.

    Supported examples:
        1234.csv
        feat_1234_formula_rank_1_fragments.csv
        feat_1234_formula_rank_1_losses.csv
        feat-1234_fragments.csv
    """

    file_name = os.path.basename(annotation_file)

    match = re.search(feat_id_pattern, file_name)

    if match is None:
        return None

    groups = [group for group in match.groups() if group is not None]

    if len(groups) == 0:
        return None

    return int(groups[0])
