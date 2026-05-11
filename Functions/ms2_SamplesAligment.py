from __future__ import annotations
from ms2_SpectralSimilarityClustering import *
import pandas as pd

def ms2_SamplesAligment(ProjectName,
                        All_SummMS2Table,
                        EdgesMat,
                        SamplesNames,
                        RT_tol = 30,
                        mz_Tol = 2e-3,
                        feature_id = 0,
                        cos_tol = 0.8,
                        min_N_ms2_spectra = 3,
                        ToReplace = 'mzML-ms2Summary.xlsx',
                        ms2Folder = 'ms2_spectra',
                        ToAdd = 'mzML',
                        Norm2One = True,
                        Intensity_to_explain = 0.9,
                        percentile = 10,
                        percentile_mz = 5,
                        percentile_Int = 10,
                        SamplingTimes = 20,
                        min_spectra_fraction = 0.3,
                        max_Nspectra_cluster = 8,
                        Nspectra_sampling = 50):
    """
    Run MS2 spectral-similarity clustering across all m/z slices.
    """

    aligned_samples_dfs = []

    for Low_id_mz, High_id_mz, slice_id in EdgesMat:
        SummMS2_raw = All_SummMS2Table[Low_id_mz: High_id_mz, :]

        AlignedSamplesDF, feature_id = ms2_SpectralSimilarityClustering(SummMS2_raw = SummMS2_raw,
                                                                        SamplesNames = SamplesNames,
                                                                        feature_id = feature_id,
                                                                        slice_id = slice_id,
                                                                        mz_col = 1,
                                                                        RT_col = 2,
                                                                        RT_tol = RT_tol,
                                                                        mz_Tol = mz_Tol,
                                                                        sample_id_col = 6,
                                                                        ms2_spec_id_col = 0,
                                                                        ms2Folder = ms2Folder,
                                                                        ToAdd = ToAdd,
                                                                        cos_tol = cos_tol,
                                                                        Norm2One = Norm2One,
                                                                        Intensity_to_explain = Intensity_to_explain,
                                                                        min_spectra_fraction = min_spectra_fraction,
                                                                        percentile = percentile,
                                                                        percentile_mz = percentile_mz,
                                                                        percentile_Int = percentile_Int,
                                                                        SamplingTimes = SamplingTimes,
                                                                        max_Nspectra_cluster = max_Nspectra_cluster,
                                                                        Nspectra_sampling = Nspectra_sampling)

        TableLoc = ProjectName + '-' + str(slice_id) + '.csv'
        # AlignedSamplesDF.to_csv(TableLoc)

        aligned_samples_dfs.append(AlignedSamplesDF)

    if len(aligned_samples_dfs) == 0:
        return pd.DataFrame()

    return pd.concat(aligned_samples_dfs,
                     ignore_index = True)