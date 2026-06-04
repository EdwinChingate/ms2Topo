from __future__ import annotations

def adjacency_clustering(context,
                         params):
    """
    Recursively collect one connected module from an adjacency list.

    Expected context keys:
        node_id, adjacency_list, module
    """

    node_id = context["node_id"]
    adjacency_list = context["adjacency_list"]
    module = context["module"]

    current_module = set(adjacency_list[node_id])
    current_module = current_module - set(module)
    module = module + list(current_module)

    for neighbour_id in current_module:
        neighbour_context = {"node_id": neighbour_id,
                             "adjacency_list": adjacency_list,
                             "module": module}

        module = adjacency_clustering(context = neighbour_context,
                                      params = params)

    return module
