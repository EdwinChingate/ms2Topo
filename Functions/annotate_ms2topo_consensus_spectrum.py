from __future__ import annotations

import numpy as np
import os
import pandas as pd
from ms2topo_consensus_to_orbifrags_spectrumpeaks import *
from AnnotateSpec import *
from MoleculesCand import *
from FragSpacePos import *

def annotate_ms2topo_consensus_spectrum(consensus_df,
                                        precursor_mz,
                                        precursor_ci_ppm = 10.0,
                                        feat_id = None,
                                        mz_col = "median_mz(Da)",
                                        intensity_col = "median_Int",
                                        n_col = "N_spectra",
                                        iqr_ppm_col = "IQR_mz(ppm)",
                                        min_ci_ppm = 10.0,
                                        fallback_ci_ppm = 10.0,
                                        max_ci_ppm = 30.0,
                                        min_relative_intensity = 0.0,
                                        top_n = 10,
                                        intensity_normalization = "sum",
                                        only_product_ions = True,
                                        min_n_fragments = 2,
                                        number_of_annotations = 0,
                                        min_number_of_annotations = 5,
                                        return_spectrum_peaks = False,
                                        return_diagnostics = True,
                                        return_empty_on_fail = False):
    """
    Annotate one ms2Topo consensus MS2 spectrum with OrbiFragsNets.

    This function jumps directly from the ms2Topo consensus spectrum to the
    OrbiFragsNets annotation step.

    It also performs explicit diagnostics before calling AnnotateSpec, because
    the original OrbiFragsNets code often returns 0 when no feasible formula
    space or no feasible fragment network is found.
    """

    diagnostics = {}

    required_cols = [mz_col,
                     intensity_col,
                     n_col]

    if iqr_ppm_col is not None:
        required_cols.append(iqr_ppm_col)

    missing_cols = [col for col in required_cols if col not in consensus_df.columns]

    if len(missing_cols) > 0:
        raise ValueError(f"The following columns were not found: {missing_cols}. "
                         f"Available columns are: {list(consensus_df.columns)}")

    if precursor_mz is None:
        raise ValueError("precursor_mz cannot be None.")

    precursor_mz = float(precursor_mz)
    precursor_ci_ppm = float(precursor_ci_ppm)

    if np.isnan(precursor_mz):
        raise ValueError("precursor_mz cannot be NaN.")

    if precursor_mz <= 0:
        raise ValueError("precursor_mz must be higher than zero.")

    if precursor_ci_ppm <= 0:
        raise ValueError("precursor_ci_ppm must be higher than zero.")

    diagnostics["working_directory"] = os.getcwd()
    diagnostics["has_parameters_folder"] = os.path.isdir("Parameters")
    diagnostics["has_massvec"] = os.path.isfile("Parameters/MassVec.csv")
    diagnostics["has_max_atomic_subscripts"] = os.path.isfile("Parameters/MaxAtomicSubscripts.csv")

    if not diagnostics["has_massvec"]:
        raise FileNotFoundError("Parameters/MassVec.csv was not found from the current "
                                "working directory. OrbiFragsNets reads this file with "
                                "os.getcwd() + '/Parameters/MassVec.csv'.")

    spectrum_peaks, spectrum_peaks_df = ms2topo_consensus_to_orbifrags_spectrumpeaks(consensus_df = consensus_df,
                                                                                     mz_col = mz_col,
                                                                                     intensity_col = intensity_col,
                                                                                     n_col = n_col,
                                                                                     iqr_ppm_col = iqr_ppm_col,
                                                                                     min_ci_ppm = min_ci_ppm,
                                                                                     fallback_ci_ppm = fallback_ci_ppm,
                                                                                     max_ci_ppm = max_ci_ppm,
                                                                                     min_relative_intensity = min_relative_intensity,
                                                                                     top_n = top_n,
                                                                                     intensity_normalization = intensity_normalization,
                                                                                     sort_by_mz = True,
                                                                                     return_df = True)

    diagnostics["n_consensus_fragments"] = len(consensus_df)
    diagnostics["n_orbifrags_fragments"] = len(spectrum_peaks)
    diagnostics["precursor_mz"] = precursor_mz
    diagnostics["precursor_ci_ppm"] = precursor_ci_ppm
    diagnostics["min_fragment_mz"] = float(np.min(spectrum_peaks[:, 0]))
    diagnostics["max_fragment_mz"] = float(np.max(spectrum_peaks[:, 0]))

    if only_product_ions:
        precursor_ci_da = precursor_mz * precursor_ci_ppm / 1e6
        max_product_mz = precursor_mz + precursor_ci_da

        product_ion_loc = np.where(spectrum_peaks[:, 0] <= max_product_mz)[0]

        spectrum_peaks = spectrum_peaks[product_ion_loc, :]
        spectrum_peaks_df = spectrum_peaks_df.iloc[product_ion_loc, :].copy()
        spectrum_peaks_df = spectrum_peaks_df.reset_index(drop = True)

    diagnostics["n_product_ions"] = len(spectrum_peaks)

    if len(spectrum_peaks) < min_n_fragments:
        diagnostics["annotation_status"] = "too_few_product_ions"

        if return_empty_on_fail:
            annotation_df = pd.DataFrame()
            annotation_df.attrs.update(diagnostics)

            if return_spectrum_peaks and return_diagnostics:
                return annotation_df, spectrum_peaks_df, diagnostics

            if return_spectrum_peaks:
                return annotation_df, spectrum_peaks_df

            return annotation_df

        raise ValueError(f"Only {len(spectrum_peaks)} product ions were available. "
                         f"At least {min_n_fragments} are required. Diagnostics: "
                         f"{diagnostics}")

    parent_candidates = MoleculesCand(PeakMass = precursor_mz,
                                      ConfidenceInterval = precursor_ci_ppm)

    if type(parent_candidates) == type(0):
        diagnostics["annotation_status"] = "no_parent_formula_candidates"

        if return_empty_on_fail:
            annotation_df = pd.DataFrame()
            annotation_df.attrs.update(diagnostics)

            if return_spectrum_peaks and return_diagnostics:
                return annotation_df, spectrum_peaks_df, diagnostics

            if return_spectrum_peaks:
                return annotation_df, spectrum_peaks_df

            return annotation_df

        raise ValueError("No parent formula candidates were found. "
                         "Try increasing precursor_ci_ppm, checking the ionization/adduct, "
                         "or checking that precursor_mz is the ion m/z and not the neutral mass. "
                         f"Diagnostics: {diagnostics}")

    diagnostics["n_parent_formula_candidates"] = len(parent_candidates)

    first_parent_formula = np.array(parent_candidates[0, :12])
    fragment_candidates = FragSpacePos(SpectrumPeaks = spectrum_peaks,
                                       MaxAtomicSubscripts = first_parent_formula)

    if type(fragment_candidates) == type(0):
        diagnostics["annotation_status"] = "no_fragment_formula_candidates_for_first_parent"

    else:
        diagnostics["n_fragment_formula_candidates_first_parent"] = len(fragment_candidates)

    try:
        annotation_df = AnnotateSpec(SpectrumPeaks = spectrum_peaks,
                                     PrecursorFragmentMass = precursor_mz,
                                     ConfidenceInterval = precursor_ci_ppm,
                                     SaveAnnotation = False,
                                     NumberofAnnotations = number_of_annotations,
                                     MinNumberofAnnotations = min_number_of_annotations)

    except Exception as error:
        diagnostics["annotation_status"] = "annotation_failed"
        diagnostics["annotation_error"] = str(error)

        if return_empty_on_fail:
            annotation_df = pd.DataFrame()
            annotation_df.attrs.update(diagnostics)

            if return_spectrum_peaks and return_diagnostics:
                return annotation_df, spectrum_peaks_df, diagnostics

            if return_spectrum_peaks:
                return annotation_df, spectrum_peaks_df

            return annotation_df

        raise RuntimeError(f"AnnotateSpec failed. Diagnostics: {diagnostics}") from error

    if type(annotation_df) == type(0) or annotation_df is None:
        diagnostics["annotation_status"] = "no_annotation_found"

        if return_empty_on_fail:
            annotation_df = pd.DataFrame()
            annotation_df.attrs.update(diagnostics)

            if return_spectrum_peaks and return_diagnostics:
                return annotation_df, spectrum_peaks_df, diagnostics

            if return_spectrum_peaks:
                return annotation_df, spectrum_peaks_df

            return annotation_df

        raise ValueError(f"OrbiFragsNets did not find a valid annotation. "
                         f"Diagnostics: {diagnostics}")

    annotation_df = annotation_df.copy().reset_index(drop = True)

    diagnostics["annotation_status"] = "annotated"
    diagnostics["n_annotated_fragments"] = len(annotation_df)

    annotation_df["annotation_status"] = "annotated"
    annotation_df["precursor_mz"] = precursor_mz
    annotation_df["precursor_ci_ppm"] = precursor_ci_ppm
    annotation_df["n_consensus_fragments"] = diagnostics["n_consensus_fragments"]
    annotation_df["n_orbifrags_fragments"] = diagnostics["n_orbifrags_fragments"]
    annotation_df["n_product_ions"] = diagnostics["n_product_ions"]

    if feat_id is not None:
        annotation_df["feat_id"] = feat_id

    preferred_first_cols = ["feat_id",
                            "annotation_status",
                            "Formula",
                            "MeassuredMZ",
                            "PredictedMZ",
                            "Error",
                            "ConfidenceInterval",
                            "RelativeIntensity",
                            "Std",
                            "NumberofDataPoints",
                            "precursor_mz",
                            "precursor_ci_ppm",
                            "n_consensus_fragments",
                            "n_orbifrags_fragments",
                            "n_product_ions"]

    preferred_first_cols = [col for col in preferred_first_cols
                            if col in annotation_df.columns]

    remaining_cols = [col for col in annotation_df.columns
                      if col not in preferred_first_cols]

    annotation_df = annotation_df[preferred_first_cols + remaining_cols]
    annotation_df.attrs.update(diagnostics)

    if return_spectrum_peaks and return_diagnostics:
        return annotation_df, spectrum_peaks_df, diagnostics

    if return_spectrum_peaks:
        return annotation_df, spectrum_peaks_df

    if return_diagnostics:
        return annotation_df, diagnostics

    return annotation_df
