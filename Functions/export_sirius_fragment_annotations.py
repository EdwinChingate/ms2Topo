from __future__ import annotations

import os
import pandas as pd
import json
from get_sirius_aligned_features import *
from extract_ms2topo_feat_id_from_feature import *
from get_sirius_formula_candidates import *
from get_sirius_annotated_msms_data import *
from get_sirius_fragmentation_tree import *
from sirius_annotated_msms_to_fragment_table import *
from sirius_fragtree_to_loss_table import *

def export_sirius_fragment_annotations(base_url,
                                       project_id,
                                       output_folder,
                                       top_n_formulas = 1):
    """
    Export SIRIUS fragment annotation tables and loss tables for all features.

    One fragment table and one loss table are written per feature/formula.
    """

    os.makedirs(output_folder, exist_ok = True)

    fragments_folder = os.path.join(output_folder, "fragment_tables")
    losses_folder = os.path.join(output_folder, "loss_tables")
    raw_json_folder = os.path.join(output_folder, "raw_json")

    os.makedirs(fragments_folder, exist_ok = True)
    os.makedirs(losses_folder, exist_ok = True)
    os.makedirs(raw_json_folder, exist_ok = True)

    features = get_sirius_aligned_features(base_url = base_url,
                                           project_id = project_id)

    run_log = []

    for feature in features:

        aligned_feature_id = feature.get("alignedFeatureId",
                                         feature.get("id"))

        feat_id = extract_ms2topo_feat_id_from_feature(feature)

        if aligned_feature_id is None:
            run_log.append({
                "feat_id": feat_id,
                "aligned_feature_id": None,
                "status": "missing_aligned_feature_id",
                "error": str(feature)[:500]
            })

            continue

        try:
            formulas = get_sirius_formula_candidates(base_url = base_url,
                                                     project_id = project_id,
                                                     aligned_feature_id = aligned_feature_id)

            if len(formulas) == 0:
                run_log.append({
                    "feat_id": feat_id,
                    "aligned_feature_id": aligned_feature_id,
                    "status": "no_formula_candidates",
                    "error": ""
                })

                continue

            formulas_to_export = formulas[:top_n_formulas]

            for formula_index, formula in enumerate(formulas_to_export):

                formula_rank = formula_index + 1

                formula_id = formula.get("formulaId",
                                         formula.get("id"))

                if formula_id is None:
                    run_log.append({
                        "feat_id": feat_id,
                        "aligned_feature_id": aligned_feature_id,
                        "status": "missing_formula_id",
                        "error": str(formula)[:500]
                    })

                    continue

                annotated_msms = get_sirius_annotated_msms_data(
                    base_url = base_url,
                    project_id = project_id,
                    aligned_feature_id = aligned_feature_id,
                    formula_id = formula_id
                )

                frag_tree = get_sirius_fragmentation_tree(
                    base_url = base_url,
                    project_id = project_id,
                    aligned_feature_id = aligned_feature_id,
                    formula_id = formula_id
                )

                annotation_df = sirius_annotated_msms_to_fragment_table(
                    annotated_msms = annotated_msms,
                    feat_id = feat_id,
                    aligned_feature_id = aligned_feature_id,
                    formula_id = formula_id,
                    formula_rank = formula_rank
                )

                loss_df = sirius_fragtree_to_loss_table(
                    frag_tree = frag_tree,
                    feat_id = feat_id,
                    aligned_feature_id = aligned_feature_id,
                    formula_id = formula_id,
                    formula_rank = formula_rank
                )

                if feat_id is not None:
                    file_prefix = "feat_" + str(feat_id) + "_formula_rank_" + str(formula_rank)

                else:
                    file_prefix = "aligned_feature_" + str(aligned_feature_id) + \
                                  "_formula_rank_" + str(formula_rank)

                annotation_loc = os.path.join(fragments_folder,
                                              file_prefix + "_fragments.csv")

                loss_loc = os.path.join(losses_folder,
                                        file_prefix + "_losses.csv")

                annotated_msms_loc = os.path.join(raw_json_folder,
                                                  file_prefix + "_annotated_msms.json")

                frag_tree_loc = os.path.join(raw_json_folder,
                                             file_prefix + "_fragtree.json")

                annotation_df.to_csv(annotation_loc, index = False)
                loss_df.to_csv(loss_loc, index = False)

                with open(annotated_msms_loc, "w") as file:
                    json.dump(annotated_msms, file, indent = 2)

                with open(frag_tree_loc, "w") as file:
                    json.dump(frag_tree, file, indent = 2)

                run_log.append({
                    "feat_id": feat_id,
                    "aligned_feature_id": aligned_feature_id,
                    "formula_id": formula_id,
                    "formula_rank": formula_rank,
                    "status": "exported",
                    "n_annotated_fragments": len(annotation_df),
                    "n_losses": len(loss_df),
                    "fragment_table": annotation_loc,
                    "loss_table": loss_loc,
                    "error": ""
                })

        except Exception as error:
            run_log.append({
                "feat_id": feat_id,
                "aligned_feature_id": aligned_feature_id,
                "status": "failed",
                "error": str(error)
            })

    run_log_df = pd.DataFrame(run_log)

    run_log_df.to_csv(os.path.join(output_folder,
                                   "sirius_fragment_annotation_export_log.csv"),
                      index = False)

    return run_log_df
