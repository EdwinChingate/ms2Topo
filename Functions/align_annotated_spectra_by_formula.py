from __future__ import annotations

import pandas as pd
import os
from extract_feat_id_from_annotation_file import *

def align_annotated_spectra_by_formula(annotated_spectra_folder,
                                       annotation_files = None,
                                       formula_col = "Formula",
                                       value_col = "RelativeIntensity",
                                       feat_id_col = "feat_id",
                                       file_extension = ".csv",
                                       min_value = 0.0,
                                       aggregation = "max",
                                       fill_value = 0.0,
                                       binary_matrix = False,
                                       keep_unannotated = False,
                                       annotation_id_sep = "|",
                                       default_value = 1.0,
                                       return_long_table = False):
    """
    Align annotated MS2 spectra using formula-like annotation IDs as row IDs.

    This function works for both:

        fragment tables:
            formula_col = "Formula"
            value_col = "RelativeIntensity"

        loss tables:
            formula_col = "loss_formula"
            value_col = None

        transition tables:
            formula_col = ["source_formula", "loss_formula", "target_formula"]
            value_col = None

    Output matrix:

        rows    -> fragment formulas, loss formulas, or transition IDs
        columns -> ms2Topo feat_id
        values  -> intensity, score, or presence/absence
    """

    if not os.path.isdir(annotated_spectra_folder):
        raise FileNotFoundError(f"annotated_spectra_folder was not found: "
                                f"{annotated_spectra_folder}")

    if annotation_files is None:
        annotation_files = [os.path.join(annotated_spectra_folder, file_name)
                            for file_name in os.listdir(annotated_spectra_folder)
                            if file_name.endswith(file_extension)]

        annotation_files.sort()

    if len(annotation_files) == 0:
        raise ValueError("No annotation files were found.")

    if aggregation not in ["max",
                           "sum",
                           "mean",
                           "median",
                           "first"]:
        raise ValueError("aggregation must be one of: "
                         "'max', 'sum', 'mean', 'median', 'first'.")

    if isinstance(formula_col, str):
        formula_cols = [formula_col]

    else:
        formula_cols = list(formula_col)

    aligned_long_tables = []
    run_log = []

    for annotation_file in annotation_files:

        try:
            annotation_df = pd.read_csv(annotation_file)

            required_cols = formula_cols.copy()

            if value_col is not None:
                required_cols.append(value_col)

            missing_cols = [col for col in required_cols
                            if col not in annotation_df.columns]

            if len(missing_cols) > 0:
                run_log.append({
                    "annotation_file": annotation_file,
                    "feat_id": None,
                    "status": "missing_columns",
                    "error": str(missing_cols),
                    "n_rows": len(annotation_df)
                })

                continue

            if feat_id_col in annotation_df.columns:
                feat_id_values = annotation_df[feat_id_col].dropna().unique()

                if len(feat_id_values) > 0:
                    feat_id = int(feat_id_values[0])

                else:
                    feat_id = extract_feat_id_from_annotation_file(annotation_file)

            else:
                feat_id = extract_feat_id_from_annotation_file(annotation_file)

            if feat_id is None:
                run_log.append({
                    "annotation_file": annotation_file,
                    "feat_id": None,
                    "status": "missing_feat_id",
                    "error": "Could not recover feat_id from column or file name.",
                    "n_rows": len(annotation_df)
                })

                continue

            spectrum_df = annotation_df.copy()

            for col in formula_cols:
                spectrum_df[col] = spectrum_df[col].astype(str)

            if not keep_unannotated:
                for col in formula_cols:
                    spectrum_df = spectrum_df[spectrum_df[col].notna()].copy()
                    spectrum_df = spectrum_df[spectrum_df[col] != ""].copy()
                    spectrum_df = spectrum_df[spectrum_df[col] != "nan"].copy()
                    spectrum_df = spectrum_df[spectrum_df[col] != "None"].copy()
                    spectrum_df = spectrum_df[spectrum_df[col] != "-"].copy()

            if len(formula_cols) == 1:
                spectrum_df["annotation_id"] = spectrum_df[formula_cols[0]].astype(str)

            else:
                spectrum_df["annotation_id"] = spectrum_df[formula_cols].astype(str).agg(
                    annotation_id_sep.join,
                    axis = 1
                )

            if value_col is None:
                spectrum_df["annotation_value"] = float(default_value)

            else:
                spectrum_df["annotation_value"] = pd.to_numeric(spectrum_df[value_col],
                                                                errors = "coerce")

            spectrum_df = spectrum_df.dropna(subset = ["annotation_id",
                                                       "annotation_value"]).copy()

            if min_value > 0:
                spectrum_df = spectrum_df[spectrum_df["annotation_value"] >= min_value].copy()

            if len(spectrum_df) == 0:
                run_log.append({
                    "annotation_file": annotation_file,
                    "feat_id": feat_id,
                    "status": "no_valid_annotations",
                    "error": "",
                    "n_rows": len(annotation_df)
                })

                continue

            spectrum_df = spectrum_df[["annotation_id",
                                       "annotation_value"]].copy()

            spectrum_df["feat_id"] = feat_id

            if aggregation == "max":
                spectrum_df = spectrum_df.groupby(["annotation_id",
                                                   "feat_id"],
                                                  as_index = False)["annotation_value"].max()

            elif aggregation == "sum":
                spectrum_df = spectrum_df.groupby(["annotation_id",
                                                   "feat_id"],
                                                  as_index = False)["annotation_value"].sum()

            elif aggregation == "mean":
                spectrum_df = spectrum_df.groupby(["annotation_id",
                                                   "feat_id"],
                                                  as_index = False)["annotation_value"].mean()

            elif aggregation == "median":
                spectrum_df = spectrum_df.groupby(["annotation_id",
                                                   "feat_id"],
                                                  as_index = False)["annotation_value"].median()

            elif aggregation == "first":
                spectrum_df = spectrum_df.groupby(["annotation_id",
                                                   "feat_id"],
                                                  as_index = False)["annotation_value"].first()

            aligned_long_tables.append(spectrum_df)

            run_log.append({
                "annotation_file": annotation_file,
                "feat_id": feat_id,
                "status": "aligned",
                "error": "",
                "n_rows": len(annotation_df),
                "n_annotations_used": len(spectrum_df)
            })

        except Exception as error:

            run_log.append({
                "annotation_file": annotation_file,
                "feat_id": None,
                "status": "failed",
                "error": str(error),
                "n_rows": None
            })

    run_log_df = pd.DataFrame(run_log)

    if len(aligned_long_tables) == 0:
        raise ValueError("No annotation files could be aligned. Check run_log_df.")

    aligned_long_df = pd.concat(aligned_long_tables,
                                ignore_index = True)

    aligned_annotations_df = aligned_long_df.pivot_table(index = "annotation_id",
                                                         columns = "feat_id",
                                                         values = "annotation_value",
                                                         aggfunc = aggregation,
                                                         fill_value = fill_value)

    aligned_annotations_df = aligned_annotations_df.sort_index()
    aligned_annotations_df = aligned_annotations_df.reindex(sorted(aligned_annotations_df.columns),
                                                            axis = 1)

    if binary_matrix:
        aligned_annotations_df = (aligned_annotations_df > fill_value).astype(int)

    annotation_metadata_df = pd.DataFrame({
        "annotation_id": aligned_annotations_df.index,
        "N_features": (aligned_annotations_df > fill_value).sum(axis = 1).values,
        "Total_value": aligned_annotations_df.sum(axis = 1).values,
        "Max_value": aligned_annotations_df.max(axis = 1).values
    })

    annotation_metadata_df = annotation_metadata_df.sort_values(["N_features",
                                                                 "Total_value"],
                                                                ascending = False).reset_index(drop = True)

    if return_long_table:
        return aligned_annotations_df, annotation_metadata_df, aligned_long_df, run_log_df

    return aligned_annotations_df, annotation_metadata_df, run_log_df
