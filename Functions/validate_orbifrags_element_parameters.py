from __future__ import annotations

import pandas as pd
import os

def validate_orbifrags_element_parameters(parameters_folder = "Parameters"):
    """
    Validate that MassVec.csv and MaxAtomicSubscripts.csv describe the same
    elemental space in the same order.

    This should be executed before running OrbiFragsNets annotation.
    """

    massvec_path = os.path.join(parameters_folder, "MassVec.csv")
    maxsubs_path = os.path.join(parameters_folder, "MaxAtomicSubscripts.csv")

    if not os.path.isfile(massvec_path):
        raise FileNotFoundError(f"MassVec.csv was not found at: {massvec_path}")

    if not os.path.isfile(maxsubs_path):
        raise FileNotFoundError(f"MaxAtomicSubscripts.csv was not found at: {maxsubs_path}")

    massvec_df = pd.read_csv(massvec_path, index_col = 0)
    maxsubs_df = pd.read_csv(maxsubs_path, index_col = 0)

    mass_elements = list(massvec_df.index)
    maxsubs_elements = list(maxsubs_df.index)

    if mass_elements != maxsubs_elements:
        raise ValueError("MassVec.csv and MaxAtomicSubscripts.csv do not have "
                         "the same elements in the same order.\n"
                         f"MassVec elements: {mass_elements}\n"
                         f"MaxAtomicSubscripts elements: {maxsubs_elements}")

    if "Exact Mass" not in massvec_df.columns:
        raise ValueError("MassVec.csv must contain a column named 'Exact Mass'.")

    if "Value" not in maxsubs_df.columns:
        raise ValueError("MaxAtomicSubscripts.csv must contain a column named 'Value'.")

    if "F" in massvec_df.index:
        f_mass = float(massvec_df.loc["F", "Exact Mass"])

        if abs(f_mass - 18.99840316273) > 0.001:
            raise ValueError(f"The mass for F looks wrong: {f_mass}. "
                             "Expected approximately 18.99840316273.")

    summary_df = massvec_df.copy()
    summary_df["MaxAtomicSubscript"] = maxsubs_df["Value"]

    return summary_df
