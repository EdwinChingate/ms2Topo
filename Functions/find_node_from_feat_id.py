from __future__ import annotations

from feat_id_variants import *

def find_node_from_feat_id(G,
                           feat_id,
                           node_prefix = 'feat_'):
    """
    Find a graph node matching feat_id using several common ID conventions.
    """

    for candidate in feat_id_variants(
        feat_id=feat_id,
        node_prefix=node_prefix
    ):
        if candidate in G:
            return candidate

    return None
