from __future__ import annotations

from adjacency_clustering import *

def ms2_feat_modules(context,
                     params):
    """
    Extract connected modules from an adjacency list.

    Expected context keys:
        adjacency_list, node_ids
    """

    adjacency_list = context["adjacency_list"]
    node_ids = context["node_ids"]

    modules = []

    while len(node_ids) > 0:
        candidate_id = list(node_ids)[0]

        module_context = {"node_id": candidate_id,
                          "adjacency_list": adjacency_list,
                          "module": []}

        module = adjacency_clustering(context = module_context,
                                      params = params)

        node_ids = node_ids - set(module)
        modules.append(module)

    return modules
