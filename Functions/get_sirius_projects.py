from __future__ import annotations

from sirius_get_json import *
from normalize_sirius_list import *

def get_sirius_projects(base_url):
    """
    List open SIRIUS projects.
    """

    projects = sirius_get_json(base_url, "/api/projects")

    return normalize_sirius_list(projects)
