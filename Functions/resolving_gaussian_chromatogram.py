from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from gaussian_chromatogram import *
from show_df import *
from tools_gaussian_chrom import *

def resolving_gaussian_chromatogram(context,
                                    params):
    """
    Resolve one chromatogram into a matrix of Gaussian parameters.

    Expected context keys:
        chromatogram

    Relevant params:
        params["gaussian"]["show_error_chrom"]
        params["curve_fit"]["maxfev"]
    """

    chromatogram = context["chromatogram"]

    tools_context = {"chromatogram": chromatogram}
    s_chrom, parameters_list, bounds = tools_gaussian_chrom(context = tools_context,
                                                           params = params)

    if len(s_chrom) == 0:
        return []

    rt_vec = s_chrom[:, 0]
    int_vec = s_chrom[:, 1]

    def gaussian_chromatogram_model(rt_vec_model,
                                    *parameters_list_model):
        model_context = {"rt_vec": rt_vec_model,
                         "parameters_list": parameters_list_model}

        intensity_model = gaussian_chromatogram(context = model_context,
                                                params = params)

        return intensity_model

    try:
        gaussian_parameters_list = list(curve_fit(gaussian_chromatogram_model,
                                                  xdata = rt_vec,
                                                  ydata = int_vec,
                                                  p0 = parameters_list,
                                                  bounds = bounds,
                                                  maxfev = params["curve_fit"]["maxfev"])[0])

        n_peaks = int(len(gaussian_parameters_list) / 3)
        gaussian_parameters = np.array(gaussian_parameters_list).reshape(n_peaks,
                                                                         3)

        gaussian_parameters = gaussian_parameters[gaussian_parameters[:, 0].argsort(), :]

        return gaussian_parameters

    except Exception as error:
        if params["gaussian"]["show_error_chrom"]:
            show_context = {"df": parameters_list,
                            "columns": list(range(len(parameters_list)))}

            show_df(context = show_context,
                    params = params)

            rt_col = params["columns"]["rt_col"]
            int_col = params["columns"]["int_col"]

            plt.plot(chromatogram[:, rt_col],
                     chromatogram[:, int_col],
                     ".")

            plt.show()

        return []
