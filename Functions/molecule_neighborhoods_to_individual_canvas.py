from __future__ import annotations

from pathlib import Path
import json
import pandas as pd
from canvas_layered_layout import *
from find_seed_node import *
from safe_canvas_name import *

def molecule_neighborhoods_to_individual_canvas(G,
                                                molecules_df,
                                                output_folder,
                                                feat_id_col = 'feat_id',
                                                molecule_col = 'molecule',
                                                radius = 5,
                                                min_edge_weight = 0,
                                                weight_col = 'weight',
                                                max_nodes = 500,
                                                layout_seed = 7,
                                                canvas_scale = 900,
                                                node_width = 220,
                                                node_height = 90):
    """
    Extract molecular-network neighborhoods around molecule seeds and export
    one Obsidian .canvas file per molecule.
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

        canvas_pos = canvas_layered_layout(subG = subG,
                                           distance_dict = distance_dict,
                                           seed_node = seed_node,
                                           node_width = node_width,
                                           node_height = node_height,
                                           seed_width = 320,
                                           seed_height = 150,
                                           horizontal_gap = 220,
                                           vertical_gap = 80)

        canvas_nodes = []
        canvas_edges = []

        for node in subG.nodes():

            node_position = canvas_pos[node]

            node_distance = distance_dict.get(node,
                                              0)

            if node == seed_node:
                node_text = ("# " + str(molecule) + "\n\n" +
                             "feat_id: `" + str(node) + "`\n\n" +
                             "distance: " + str(node_distance))

            else:
                node_text = ("feat_id: `" + str(node) + "`\n\n" +
                             "distance: " + str(node_distance))

            canvas_nodes.append({"id": str(node),
                                 "type": "text",
                                 "text": node_text,
                                 "x": node_position["x"],
                                 "y": node_position["y"],
                                 "width": node_position["width"],
                                 "height": node_position["height"]})

        edge_id = 0

        for node_1, node_2, edge_data in subG.edges(data = True):

            edge_weight = edge_data.get(weight_col,
                                        1)

            if edge_weight < min_edge_weight:
                continue

            if canvas_pos[node_1]["x"] <= canvas_pos[node_2]["x"]:
                from_node = node_1
                to_node = node_2
                from_side = "right"
                to_side = "left"

            else:
                from_node = node_2
                to_node = node_1
                from_side = "right"
                to_side = "left"

            canvas_edges.append({"id": "edge_" + str(edge_id),
                                 "fromNode": str(from_node),
                                 "fromSide": from_side,
                                 "toNode": str(to_node),
                                 "toSide": to_side,
                                 "label": str(round(float(edge_weight), 4))})

            edge_id += 1

        canvas_data = {"nodes": canvas_nodes,
                       "edges": canvas_edges}

        canvas_name = (safe_canvas_name(molecule) +
                       "_feat_" +
                       safe_canvas_name(seed_node) +
                       ".canvas")

        output_canvas = output_folder / canvas_name

        with open(output_canvas,
                  "w",
                  encoding = "utf-8") as file:
            json.dump(canvas_data,
                      file,
                      indent = 2)

        summary_rows[molecule] = {"molecule": molecule,
                                  "feat_id": feat_id,
                                  "seed_node": seed_node,
                                  "n_nodes": subG.number_of_nodes(),
                                  "n_edges": subG.number_of_edges(),
                                  "output_canvas": str(output_canvas)}

    summary_df = pd.DataFrame(list(summary_rows.values()))

    return {"subnetworks": subnetworks,
            "summary_df": summary_df}
