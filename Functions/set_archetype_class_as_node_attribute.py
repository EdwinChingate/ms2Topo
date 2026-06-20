from __future__ import annotations

import networkx as nx
import pandas as pd
from find_node_from_feat_id import *
from sanitize_attribute_name import *

def set_archetype_class_as_node_attribute(G,
                                          assignments_df,
                                          feat_id_col = 'feat_id',
                                          class_col = 'best_archetype',
                                          assigned_class_attr = 'assigned_class',
                                          node_prefix = 'feat_',
                                          include_scores = True,
                                          include_pattern_cols = True,
                                          overwrite = True):
    """
    Add archetype-assignment information from assignments_df as NetworkX
    node attributes.

    Parameters
    ----------
    G:
        NetworkX graph.

    assignments_df:
        DataFrame containing at least feat_id and best_archetype.

    feat_id_col:
        Column in assignments_df with feature IDs.

    class_col:
        Column defining the assigned archetype class.

    assigned_class_attr:
        Name of the NetworkX node attribute to create.

    node_prefix:
        Prefix used if graph nodes look like "feat_3515".

    include_scores:
        If True, also add best_score, second_score, assignment_margin,
        and n_active_sample_types.

    include_pattern_cols:
        If True, also add the binary archetype-pattern columns.

    overwrite:
        If False, existing attributes with the same name are preserved.

    Returns
    -------
    G:
        Same graph object, modified in place.

    report:
        Dictionary with matching summary.
    """

    required_cols = [feat_id_col, class_col]

    missing_required = [
        col
        for col in required_cols
        if col not in assignments_df.columns
    ]

    if len(missing_required) > 0:
        raise ValueError(
            f"Missing required columns in assignments_df: {missing_required}"
        )

    score_cols = [
        "best_score",
        "second_score",
        "assignment_margin",
        "n_active_sample_types"
    ]

    metadata_cols = [
        "Unnamed: 0",
        feat_id_col,
        class_col,
        *score_cols
    ]

    pattern_cols = [
        col
        for col in assignments_df.columns
        if col not in metadata_cols
    ]

    matched_nodes = []
    unmatched_feat_ids = []
    attrs_by_node = {}

    for _, row in assignments_df.iterrows():

        feat_id = row[feat_id_col]

        node = find_node_from_feat_id(
            G=G,
            feat_id=feat_id,
            node_prefix=node_prefix
        )

        if node is None:
            unmatched_feat_ids.append(feat_id)
            continue

        node_attrs = {}

        if overwrite or assigned_class_attr not in G.nodes[node]:
            node_attrs[assigned_class_attr] = row[class_col]

        node_attrs["assignment_feat_id"] = feat_id

        if include_scores:

            for col in score_cols:

                if col not in assignments_df.columns:
                    continue

                attr_name = f"archetype_{col}"

                if overwrite or attr_name not in G.nodes[node]:
                    value = row[col]

                    if pd.isna(value):
                        value = None

                    node_attrs[attr_name] = value

        if include_pattern_cols:

            for col in pattern_cols:

                attr_name = f"archetype_pattern_{sanitize_attribute_name(col)}"

                if overwrite or attr_name not in G.nodes[node]:
                    value = row[col]

                    if pd.isna(value):
                        value = 0

                    node_attrs[attr_name] = int(value)

        attrs_by_node[node] = node_attrs
        matched_nodes.append(node)

    nx.set_node_attributes(
        G,
        attrs_by_node
    )

    report = {
        "n_graph_nodes": G.number_of_nodes(),
        "n_assignment_rows": len(assignments_df),
        "n_matched_nodes": len(matched_nodes),
        "n_unmatched_feat_ids": len(unmatched_feat_ids),
        "unmatched_feat_ids": unmatched_feat_ids
    }

    return G, report
