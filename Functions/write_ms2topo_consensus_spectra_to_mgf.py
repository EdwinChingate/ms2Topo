from __future__ import annotations

import os
import pandas as pd

def write_ms2topo_consensus_spectra_to_mgf(molecular_networking_features,
                                           consensus_spectra_folder,
                                           output_mgf,
                                           mz_col = "median_mz(Da)",
                                           intensity_col = "median_Int",
                                           feature_id_col = "feat_id",
                                           precursor_mz_col = "median_mz(Da)",
                                           charge = "1+",
                                           mslevel = 2,
                                           min_relative_intensity = 1.0,
                                           top_n = None,
                                           normalize_intensity = True):
    """
    Write ms2Topo consensus MS2 spectra into one SIRIUS-compatible MGF file.

    Each feature becomes one BEGIN IONS block. FEATURE_ID is used to map
    SIRIUS results back to the ms2Topo feat_id.
    """

    required_cols = [feature_id_col,
                     precursor_mz_col]

    missing_cols = [col for col in required_cols
                    if col not in molecular_networking_features.columns]

    if len(missing_cols) > 0:
        raise ValueError(f"The following columns were not found: {missing_cols}. "
                         f"Available columns are: {list(molecular_networking_features.columns)}")

    os.makedirs(os.path.dirname(output_mgf), exist_ok = True)

    run_log = []

    with open(output_mgf, "w") as mgf_file:

        for feature_table_index in molecular_networking_features.index:

            feat_id = int(molecular_networking_features.loc[feature_table_index, feature_id_col])
            precursor_mz = float(molecular_networking_features.loc[feature_table_index, precursor_mz_col])

            consensus_spectrum_loc = os.path.join(
                consensus_spectra_folder,
                "Consensus_ms2-spectra_" + str(feat_id) + ".csv"
            )

            if not os.path.isfile(consensus_spectrum_loc):
                run_log.append({
                    "feat_id": feat_id,
                    "status": "missing_consensus_spectrum",
                    "consensus_spectrum_loc": consensus_spectrum_loc,
                    "n_fragments_written": 0
                })

                continue

            consensus_df = pd.read_csv(consensus_spectrum_loc, index_col = 0)

            spectrum_missing_cols = [col for col in [mz_col, intensity_col]
                                     if col not in consensus_df.columns]

            if len(spectrum_missing_cols) > 0:
                run_log.append({
                    "feat_id": feat_id,
                    "status": "missing_spectrum_columns",
                    "consensus_spectrum_loc": consensus_spectrum_loc,
                    "missing_columns": str(spectrum_missing_cols),
                    "n_fragments_written": 0
                })

                continue

            spectrum_df = consensus_df[[mz_col, intensity_col]].copy()
            spectrum_df.columns = ["fragment_mz", "fragment_intensity"]

            spectrum_df = spectrum_df.dropna(subset = ["fragment_mz",
                                                       "fragment_intensity"]).copy()

            spectrum_df = spectrum_df[spectrum_df["fragment_intensity"] > 0].copy()
            spectrum_df = spectrum_df[spectrum_df["fragment_mz"] < precursor_mz].copy()

            if len(spectrum_df) == 0:
                run_log.append({
                    "feat_id": feat_id,
                    "status": "no_valid_fragments",
                    "consensus_spectrum_loc": consensus_spectrum_loc,
                    "n_fragments_written": 0
                })

                continue

            if normalize_intensity:
                spectrum_df["relative_intensity"] = spectrum_df["fragment_intensity"] / \
                                                    spectrum_df["fragment_intensity"].max() * 100

            else:
                spectrum_df["relative_intensity"] = spectrum_df["fragment_intensity"]

            if min_relative_intensity > 0:
                spectrum_df = spectrum_df[spectrum_df["relative_intensity"] >=
                                          min_relative_intensity].copy()

            if top_n is not None:
                spectrum_df = spectrum_df.sort_values("relative_intensity",
                                                      ascending = False).head(top_n).copy()

            spectrum_df = spectrum_df.sort_values("fragment_mz").reset_index(drop = True)

            if len(spectrum_df) == 0:
                run_log.append({
                    "feat_id": feat_id,
                    "status": "no_fragments_after_filtering",
                    "consensus_spectrum_loc": consensus_spectrum_loc,
                    "n_fragments_written": 0
                })

                continue

            mgf_file.write("BEGIN IONS\n")
            mgf_file.write(f"FEATURE_ID={feat_id}\n")
            mgf_file.write(f"TITLE=ms2Topo_feat_{feat_id}\n")
            mgf_file.write(f"PEPMASS={precursor_mz:.8f}\n")
            mgf_file.write(f"CHARGE={charge}\n")
            mgf_file.write(f"MSLEVEL={mslevel}\n")

            for _, row in spectrum_df.iterrows():
                mgf_file.write(f"{row['fragment_mz']:.8f} {row['relative_intensity']:.6f}\n")

            mgf_file.write("END IONS\n\n")

            run_log.append({
                "feat_id": feat_id,
                "status": "written",
                "consensus_spectrum_loc": consensus_spectrum_loc,
                "n_fragments_written": len(spectrum_df)
            })

    run_log_df = pd.DataFrame(run_log)

    return run_log_df
