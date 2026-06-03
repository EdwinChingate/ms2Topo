from __future__ import annotations

from sirius_get_json import *
from normalize_sirius_list import *

def get_sirius_aligned_features(base_url,
                                project_id):
    """
    List aligned features in a SIRIUS project.
    """

    endpoint = "/api/projects/" + str(project_id) + "/aligned-features"

    features = sirius_get_json(base_url, endpoint)

    return normalize_sirius_list(features)
