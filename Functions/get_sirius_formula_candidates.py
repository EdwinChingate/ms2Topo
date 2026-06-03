from __future__ import annotations

from sirius_get_json import *
from normalize_sirius_list import *

def get_sirius_formula_candidates(base_url,
                                  project_id,
                                  aligned_feature_id):
    """
    List molecular formula candidates for one aligned feature.
    """

    endpoint = "/api/projects/" + str(project_id) + \
               "/aligned-features/" + str(aligned_feature_id) + \
               "/formulas"

    formulas = sirius_get_json(base_url, endpoint)

    return normalize_sirius_list(formulas)
