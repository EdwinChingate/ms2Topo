from __future__ import annotations

import os
from AllSubChromatograms import *
from GaussianParametersTable import *

from resolving_gaussian_chromatogram import *

def resolve_full_chromatogram(context,
                              params):
    """
    Resolve all sub-chromatograms associated with one m/z feature.

    Expected context keys:
        mz, mz_std, all_raw_peaks

    Relevant params:
        params["chromatogram"]["std_distance"]
        params["chromatogram"]["rt_tol"]
        params["chromatogram"]["min_signals"]
        params["output"]["save_peaks"]
        params["output"]["output_folder"]
        params["output"]["mz_name"]
    """

    mz = context["mz"]
    mz_std = context["mz_std"]
    all_raw_peaks = context["all_raw_peaks"]

    chromatogram_list = AllSubChromatograms(mz = mz,
                                            mz_std = mz_std,
                                            AllRawPeaks = all_raw_peaks,
                                            stdDistance = params["chromatogram"]["std_distance"],
                                            RT_tol = params["chromatogram"]["rt_tol"],
                                            minSignals = params["chromatogram"]["min_signals"])

    gaussian_parameters_list = []

    for chromatogram in chromatogram_list:
        chromatogram_context = {"chromatogram": chromatogram}

        gaussian_parameters = resolving_gaussian_chromatogram(context = chromatogram_context,
                                                              params = params)

        if len(gaussian_parameters) > 0:
            gaussian_parameters_list.append([gaussian_parameters,
                                             chromatogram])

    if params["output"]["save_peaks"]:
        gaussian_parameters_df = GaussianParametersTable(GaussianParametersList = gaussian_parameters_list)

        output_file = os.path.join(params["output"]["output_folder"],
                                   str(mz) + params["output"]["mz_name"] + ".xlsx")

        gaussian_parameters_df.to_excel(output_file)

    return gaussian_parameters_list
