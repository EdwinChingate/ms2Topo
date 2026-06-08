from __future__ import annotations

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from find_seed_node import *

def draw_molecule_neighborhoods(G,
                                molecules_df,
                                feat_id_col = "feat_id",
                                molecule_col = "molecule",
                                radius = 5,
                                min_edge_weight = 0,
                                weight_col = "weight",
                                max_nodes = 500,
                                layout_seed = 7):
    """
    Extract and draw the network neighborhood around each molecule seed.
    """

    summary_rows = {}
    subnetworks = {}

    for row_id in molecules_df.index:

        molecule = molecules_df.loc[row_id, molecule_col]
        feat_id = molecules_df.loc[row_id, feat_id_col]

        seed_node = find_seed_node(G,
                                   feat_id)

        if seed_node is None:
            print(str(molecule) + " | feat_id " + str(feat_id) + " not found in graph")
            continue

        visited = {seed_node}
        current_layer = {seed_node}
        distance_dict = {seed_node: 0}

        for layer_id in range(1,
                              radius + 1):

            next_layer = set()

            for node in current_layer:

                for neighbor in G.neighbors(node):

                    if neighbor in visited:
                        continue

                    edge_data = G.get_edge_data(node,
                                                neighbor)

                    edge_weight = edge_data.get(weight_col,
                                                1)

                    if edge_weight < min_edge_weight:
                        continue

                    next_layer.add(neighbor)

            if len(next_layer) == 0:
                break

            if len(visited) + len(next_layer) > max_nodes:
                print(str(molecule) + " | stopped at layer " + str(layer_id) + " because max_nodes was reached")
                break

            for node in next_layer:
                distance_dict[node] = layer_id

            visited.update(next_layer)
            current_layer = next_layer

        subG = G.subgraph(list(visited)).copy()
        subnetworks[molecule] = subG

        summary_rows[molecule] = {"molecule": molecule,
                                  "feat_id": feat_id,
                                  "seed_node": seed_node,
                                  "n_nodes": subG.number_of_nodes(),
                                  "n_edges": subG.number_of_edges()}

        if subG.number_of_nodes() == 0:
            continue

        plt.figure(figsize = (8, 6))

        pos = nx.spring_layout(subG,
                               seed = layout_seed,
                               weight = weight_col)

        node_colors = [distance_dict.get(node, 0)
                       for node in subG.nodes()]

        edge_widths = []

        for node_1, node_2, edge_data in subG.edges(data = True):
            edge_widths.append(0.5 + 3 * edge_data.get(weight_col, 1))

        nx.draw_networkx_edges(subG,
                               pos,
                               alpha = 0.35,
                               width = edge_widths)

        nx.draw_networkx_nodes(subG,
                               pos,
                               node_size = 120,
                               node_color = node_colors,
                               cmap = "viridis")

        nx.draw_networkx_labels(subG,
                                pos,
                                font_size = 7)

        plt.title(str(molecule) + " | seed " + str(seed_node) +
                  " | nodes " + str(subG.number_of_nodes()) +
                  " | edges " + str(subG.number_of_edges()))

        plt.axis("off")
        plt.show()

    summary_df = pd.DataFrame(list(summary_rows.values()))

    return {"subnetworks": subnetworks,
            "summary_df": summary_df}
