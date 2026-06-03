from __future__ import annotations

from sirius_get_json import *

def get_sirius_annotated_msms_data(base_url,
                                   project_id,
                                   aligned_feature_id,
                                   formula_id):
    """
    Retrieve annotated MS/MS data for one feature/formula.
    """

    endpoint = "/api/projects/" + str(project_id) + \
               "/aligned-features/" + str(aligned_feature_id) + \
               "/formulas/" + str(formula_id) + \
               "/annotated-msmsdata"

    return sirius_get_json(base_url, endpoint)
