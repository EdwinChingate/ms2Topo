from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from find_seed_node import *

def draw_molecule_archetype_frontiers(G,
                                      molecules_df,
                                      forbidden_terms = ('EffluentClean',),
                                      feat_id_col = 'feat_id',
                                      molecule_col = 'molecule',
                                      archetype_attr = 'best_archetype',
                                      idf_attr = "weighted_mean_fragment_IDF",
                                      stop_at_lower_idf = True,
                                      idf_tolerance = 0,
                                      missing_idf_policy = "allow",
                                      min_edge_weight = 0,
                                      weight_col = 'weight',
                                      max_nodes = 500,
                                      include_boundary = True,
                                      layout_seed = 7):
    """
    Walk from each molecule seed through nodes whose archetype does not contain
    any forbidden term, and optionally stop expanding paths when a neighbor has
    lower IDF than the current node.

    Example:
        forbidden_terms=("EffluentClean",)

    rejects:
        EffluentClean | Histidine
        EffluentClean | Aniline
        Effluent | Histidine + EffluentClean | Succinate

    If stop_at_lower_idf is True:
        a neighbor with lower IDF than the current node can be included as a
        boundary node, but it is not expanded.

    The seed node is allowed regardless of its own archetype.
    Forbidden nodes and lower-IDF nodes can be included as boundary nodes but
    are not expanded.
    """

    summary_rows = {}
    subnetworks = {}

    for row_id in molecules_df.index:

        molecule = molecules_df.loc[row_id, molecule_col]
        feat_id = molecules_df.loc[row_id, feat_id_col]

        seed_node = find_seed_node(G, feat_id)

        if seed_node is None:
            print(str(molecule) + " | feat_id " + str(feat_id) + " not found in graph")
            continue

        visited = {seed_node}
        expandable = {seed_node}

        distance_dict = {seed_node: 0}
        role_dict = {seed_node: "seed"}

        while len(expandable) > 0:

            next_expandable = set()
            stop_now = False

            for node in expandable:

                for neighbor in G.neighbors(node):

                    if neighbor in visited:
                        continue

                    edge_data = G.get_edge_data(node, neighbor)
                    edge_weight = edge_data.get(weight_col, 1)

                    if edge_weight < min_edge_weight:
                        continue

                    if len(visited) + 1 > max_nodes:
                        print(str(molecule) + " | stopped because max_nodes was reached")
                        stop_now = True
                        break

                    neighbor_archetype = G.nodes[neighbor].get(archetype_attr, "")

                    neighbor_is_forbidden = archetype_has_forbidden_term(
                        neighbor_archetype,
                        forbidden_terms = forbidden_terms
                    )

                    neighbor_is_lower_idf = False

                    if stop_at_lower_idf:

                        neighbor_is_lower_idf = neighbor_has_lower_idf(
                            G = G,
                            node = node,
                            neighbor = neighbor,
                            idf_attr = idf_attr,
                            idf_tolerance = idf_tolerance,
                            missing_idf_policy = missing_idf_policy
                        )

                    if (not neighbor_is_forbidden) and (not neighbor_is_lower_idf):

                        visited.add(neighbor)
                        next_expandable.add(neighbor)

                        distance_dict[neighbor] = distance_dict[node] + 1
                        role_dict[neighbor] = "allowed"

                    else:

                        if include_boundary:

                            visited.add(neighbor)

                            distance_dict[neighbor] = distance_dict[node] + 1

                            if neighbor_is_forbidden and neighbor_is_lower_idf:
                                role_dict[neighbor] = "boundary_forbidden_lower_idf"

                            elif neighbor_is_forbidden:
                                role_dict[neighbor] = "boundary_forbidden"

                            elif neighbor_is_lower_idf:
                                role_dict[neighbor] = "boundary_lower_idf"

                        # Boundary nodes are not expanded.

                if stop_now:
                    break

            if stop_now:
                break

            expandable = next_expandable

        subG = G.subgraph(list(visited)).copy()

        weak_edges = [
            (node_1, node_2)
            for node_1, node_2, edge_data in subG.edges(data = True)
            if edge_data.get(weight_col, 1) < min_edge_weight
        ]

        subG.remove_edges_from(weak_edges)
        subnetworks[molecule] = subG

        for node in subG.nodes():

            subG.nodes[node]["frontier_distance"] = distance_dict.get(node, np.nan)
            subG.nodes[node]["frontier_role"] = role_dict.get(node, "unknown")

        n_allowed = sum([
            role_dict.get(node) == "allowed"
            for node in subG.nodes()
        ])

        n_boundary_forbidden = sum([
            role_dict.get(node) == "boundary_forbidden"
            for node in subG.nodes()
        ])

        n_boundary_lower_idf = sum([
            role_dict.get(node) == "boundary_lower_idf"
            for node in subG.nodes()
        ])

        n_boundary_forbidden_lower_idf = sum([
            role_dict.get(node) == "boundary_forbidden_lower_idf"
            for node in subG.nodes()
        ])

        summary_rows[molecule] = {
            "molecule": molecule,
            "feat_id": feat_id,
            "seed_node": seed_node,
            "seed_archetype": G.nodes[seed_node].get(archetype_attr, np.nan),
            "seed_idf": G.nodes[seed_node].get(idf_attr, np.nan),
            "n_nodes": subG.number_of_nodes(),
            "n_edges": subG.number_of_edges(),
            "n_allowed": n_allowed,
            "n_boundary_forbidden": n_boundary_forbidden,
            "n_boundary_lower_idf": n_boundary_lower_idf,
            "n_boundary_forbidden_lower_idf": n_boundary_forbidden_lower_idf
        }

        plt.figure(figsize=(8, 6))

        pos = nx.spring_layout(
            subG,
            seed = layout_seed,
            weight = weight_col
        )

        color_dict = {
            "seed": "red",
            "allowed": "mediumseagreen",
            "boundary_forbidden": "lightgray",
            "boundary_lower_idf": "cornflowerblue",
            "boundary_forbidden_lower_idf": "plum",
            "unknown": "white"
        }

        node_colors = [
            color_dict.get(
                subG.nodes[node].get("frontier_role", "unknown"),
                "white"
            )
            for node in subG.nodes()
        ]

        edge_widths = [
            0.5 + 3 * edge_data.get(weight_col, 1)
            for _, _, edge_data in subG.edges(data = True)
        ]

        nx.draw_networkx_edges(
            subG,
            pos,
            alpha = 0.35,
            width = edge_widths
        )

        nx.draw_networkx_nodes(
            subG,
            pos,
            node_size = 120,
            node_color = node_colors,
            edgecolors = "black",
            linewidths = 0.4
        )

        nx.draw_networkx_labels(
            subG,
            pos,
            font_size = 7
        )

        plt.title(
            str(molecule)
            + " | seed " + str(seed_node)
            + " | nodes " + str(subG.number_of_nodes())
            + " | allowed " + str(n_allowed)
            + " | forbidden " + str(n_boundary_forbidden)
            + " | lower IDF " + str(n_boundary_lower_idf)
        )

        plt.axis("off")
        plt.show()

    summary_df = pd.DataFrame(list(summary_rows.values()))

    return {
        "subnetworks": subnetworks,
        "summary_df": summary_df
    }
