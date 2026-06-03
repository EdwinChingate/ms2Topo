from __future__ import annotations

import pandas as pd

def sirius_fragtree_to_loss_table(frag_tree,
                                  feat_id = None,
                                  aligned_feature_id = None,
                                  formula_id = None,
                                  formula_rank = None):
    """
    Convert a SIRIUS fragmentation tree into a loss/edge table.

    This is the table you will later want for neutral-loss Tanimoto.
    """

    fragments = frag_tree.get("fragments", [])
    losses = frag_tree.get("losses", [])

    fragments_by_index = {}

    for index, fragment in enumerate(fragments):
        fragment_id = fragment.get("fragmentId", index)
        fragments_by_index[index] = fragment
        fragments_by_index[fragment_id] = fragment

    rows = []

    for loss in losses:

        source_idx = loss.get("sourceFragmentIdx", None)
        target_idx = loss.get("targetFragmentIdx", None)

        source_fragment = fragments_by_index.get(source_idx, {})
        target_fragment = fragments_by_index.get(target_idx, {})

        row = {
            "feat_id": feat_id,
            "aligned_feature_id": aligned_feature_id,
            "formula_id": formula_id,
            "formula_rank": formula_rank,

            "source_fragment_idx": source_idx,
            "target_fragment_idx": target_idx,

            "source_formula": source_fragment.get("molecularFormula", None),
            "target_formula": target_fragment.get("molecularFormula", None),

            "source_mz": source_fragment.get("mz", None),
            "target_mz": target_fragment.get("mz", None),

            "loss_formula": loss.get("molecularFormula", None),
            "loss_score": loss.get("score", None)
        }

        rows.append(row)

    loss_df = pd.DataFrame(rows)

    return loss_df
