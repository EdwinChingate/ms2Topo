from __future__ import annotations

from pathlib import Path
import pandas as pd
from pyvis.network import Network
from find_seed_node import *
from safe_html_name import *

def molecule_neighborhoods_to_individual_html(G,
                                              molecules_df,
                                              output_folder,
                                              feat_id_col = 'feat_id',
                                              molecule_col = 'molecule',
                                              radius = 5,
                                              min_edge_weight = 0,
                                              weight_col = 'weight',
                                              max_nodes = 500,
                                              layout_seed = 7):
    """
    Extract molecular-network neighborhoods around molecule seeds and export
    one interactive HTML file per molecule.
    """

    output_folder = Path(output_folder)
    output_folder.mkdir(parents = True,
                        exist_ok = True)

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

        weak_edges = [
            (node_1, node_2)
            for node_1, node_2, edge_data in subG.edges(data = True)
            if edge_data.get(weight_col, 1) < min_edge_weight
        ]

        subG.remove_edges_from(weak_edges)
        subnetworks[molecule] = subG

        html_name = (safe_html_name(molecule) +
                     "_feat_" +
                     safe_html_name(seed_node) +
                     ".html")

        output_html = output_folder / html_name

        net = Network(height = "850px",
                      width = "100%",
                      bgcolor = "#ffffff",
                      font_color = "#222222",
                      notebook = False)

        net.force_atlas_2based()

        for node in subG.nodes():

            node_distance = distance_dict.get(node,
                                              0)

            if node == seed_node:
                node_label = str(molecule) + "\n" + str(node)
                node_title = ("seed molecule: " + str(molecule) +
                              "<br>feat_id: " + str(node) +
                              "<br>distance: " + str(node_distance))
                node_size = 30
                node_color = "#d62728"

            else:
                node_label = str(node)
                node_title = ("feat_id: " + str(node) +
                              "<br>distance: " + str(node_distance))
                node_size = max(8,
                                18 - 2 * node_distance)
                node_color = "#1f77b4"

            net.add_node(str(node),
                         label = node_label,
                         title = node_title,
                         size = node_size,
                         color = node_color)

        for node_1, node_2, edge_data in subG.edges(data = True):

            edge_weight = edge_data.get(weight_col,
                                        1)

            net.add_edge(str(node_1),
                         str(node_2),
                         value = float(edge_weight),
                         title = weight_col + ": " + str(edge_weight))

        net.write_html(str(output_html),
                       notebook = False)

        summary_rows[molecule] = {"molecule": molecule,
                                  "feat_id": feat_id,
                                  "seed_node": seed_node,
                                  "n_nodes": subG.number_of_nodes(),
                                  "n_edges": subG.number_of_edges(),
                                  "output_html": str(output_html)}

    summary_df = pd.DataFrame(list(summary_rows.values()))

    return {"subnetworks": subnetworks,
            "summary_df": summary_df}
