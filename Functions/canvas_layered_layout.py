from __future__ import annotations

def canvas_layered_layout(subG,
                          distance_dict,
                          seed_node,
                          node_width = 240,
                          node_height = 110,
                          seed_width = 320,
                          seed_height = 150,
                          horizontal_gap = 220,
                          vertical_gap = 80):
    """
    Build readable Obsidian Canvas coordinates using network distance layers.

    Output coordinates are top-left x/y positions, already accounting for
    card width and height.
    """

    layers = {}

    for node in subG.nodes():

        node_distance = distance_dict.get(node,
                                          0)

        if node_distance not in layers:
            layers[node_distance] = []

        layers[node_distance].append(node)

    canvas_pos = {}

    for layer_id in sorted(layers.keys()):

        layer_nodes = layers[layer_id]

        layer_nodes = sorted(layer_nodes,
                             key = lambda node: subG.degree(node),
                             reverse = True)

        x_pos = layer_id * (node_width + horizontal_gap)

        layer_card_heights = []

        for node in layer_nodes:

            if node == seed_node:
                layer_card_heights.append(seed_height)

            else:
                layer_card_heights.append(node_height)

        total_layer_height = (sum(layer_card_heights) +
                              vertical_gap * (len(layer_nodes) - 1))

        y_pos = -total_layer_height / 2

        for node_id, node in enumerate(layer_nodes):

            if node == seed_node:
                current_width = seed_width
                current_height = seed_height

            else:
                current_width = node_width
                current_height = node_height

            canvas_pos[node] = {"x": int(x_pos),
                                "y": int(y_pos),
                                "width": current_width,
                                "height": current_height}

            y_pos = y_pos + current_height + vertical_gap

    return canvas_pos
