from __future__ import annotations

import pandas as pd

def sirius_annotated_msms_to_fragment_table(annotated_msms,
                                            feat_id = None,
                                            aligned_feature_id = None,
                                            formula_id = None,
                                            formula_rank = None,
                                            use_merged_ms2 = True):
    """
    Convert SIRIUS annotated-msmsdata JSON into a fragment annotation table.

    Output is intentionally similar to an OrbiFragsNets annotation table:
        Formula, MeassuredMZ, PredictedMZ, Error, RelativeIntensity
    plus SIRIUS-specific columns.
    """

    if use_merged_ms2 and annotated_msms.get("mergedMs2", None) is not None:
        spectrum = annotated_msms["mergedMs2"]

    else:
        ms2_spectra = annotated_msms.get("ms2Spectra", [])

        if len(ms2_spectra) == 0:
            return pd.DataFrame()

        spectrum = ms2_spectra[0]

    peaks = spectrum.get("peaks", [])

    rows = []

    raw_intensities = [peak.get("intensity", 0) for peak in peaks
                       if peak.get("intensity", None) is not None]

    if len(raw_intensities) > 0 and max(raw_intensities) > 0:
        max_intensity = max(raw_intensities)

    else:
        max_intensity = 1.0

    spectrum_annotation = spectrum.get("spectrumAnnotation", {})

    precursor_formula = spectrum_annotation.get("molecularFormula", None)
    precursor_adduct = spectrum_annotation.get("adduct", None)

    for peak in peaks:

        peak_annotation = peak.get("peakAnnotation", None)

        if peak_annotation is None:
            peak_annotation = {}

        measured_mz = peak.get("mz", None)
        intensity = peak.get("intensity", None)

        if intensity is not None:
            relative_intensity = intensity / max_intensity * 100

        else:
            relative_intensity = None

        row = {
            "feat_id": feat_id,
            "aligned_feature_id": aligned_feature_id,
            "formula_id": formula_id,
            "formula_rank": formula_rank,
            "precursor_formula": precursor_formula,
            "precursor_adduct": precursor_adduct,

            "Formula": peak_annotation.get("molecularFormula", None),
            "Adduct": peak_annotation.get("adduct", None),
            "fragment_id": peak_annotation.get("fragmentId", None),

            "MeassuredMZ": measured_mz,
            "PredictedMZ": peak_annotation.get("exactMass", None),
            "Error": peak_annotation.get("massDeviationPpm", None),
            "Error_mDa": peak_annotation.get("massDeviationMz", None),
            "RecalibratedError": peak_annotation.get("recalibratedMassDeviationPpm", None),
            "RecalibratedError_mDa": peak_annotation.get("recalibratedMassDeviationMz", None),

            "Intensity": intensity,
            "RelativeIntensity": relative_intensity
        }

        rows.append(row)

    annotation_df = pd.DataFrame(rows)

    annotation_df = annotation_df[annotation_df["Formula"].notna()].copy()
    annotation_df = annotation_df.reset_index(drop = True)

    preferred_first_cols = ["feat_id",
                            "Formula",
                            "MeassuredMZ",
                            "PredictedMZ",
                            "Error",
                            "RelativeIntensity",
                            "Adduct",
                            "fragment_id",
                            "precursor_formula",
                            "precursor_adduct",
                            "Intensity",
                            "Error_mDa",
                            "RecalibratedError",
                            "RecalibratedError_mDa",
                            "aligned_feature_id",
                            "formula_id",
                            "formula_rank"]

    preferred_first_cols = [col for col in preferred_first_cols
                            if col in annotation_df.columns]

    remaining_cols = [col for col in annotation_df.columns
                      if col not in preferred_first_cols]

    annotation_df = annotation_df[preferred_first_cols + remaining_cols]

    return annotation_df
