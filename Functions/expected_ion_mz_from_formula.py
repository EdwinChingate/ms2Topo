from __future__ import annotations

from exact_mass_from_formula import *

def expected_ion_mz_from_formula(formula,
                                 ionization_mode = "positive",
                                 adduct = None):
    """
    Calculate expected precursor m/z from a neutral molecular formula.

    Default adducts:
        positive -> [M+H]+
        negative -> [M-H]-
        neutral  -> M
    """
    PROTON_MASS = 1.007276466621

    ADDUCT_MASS_SHIFTS = {"positive": {"[M+H]+": PROTON_MASS,
                                       "[M+Na]+": 22.989218,
                                       "[M+K]+": 38.963158,
                                       "[M+NH4]+": 18.033823},
                          "negative": {"[M-H]-": -PROTON_MASS},
                          "neutral": {"M": 0.0}}

    ionization_mode = ionization_mode.lower().strip()

    if ionization_mode not in ADDUCT_MASS_SHIFTS:
        raise ValueError(f"ionization_mode must be one of {list(ADDUCT_MASS_SHIFTS.keys())}. "
                         f"Received: {ionization_mode}")

    if adduct is None:
        if ionization_mode == "positive":
            adduct = "[M+H]+"

        elif ionization_mode == "negative":
            adduct = "[M-H]-"

        elif ionization_mode == "neutral":
            adduct = "M"

    if adduct not in ADDUCT_MASS_SHIFTS[ionization_mode]:
        raise ValueError(f"Adduct '{adduct}' is not available for ionization_mode='{ionization_mode}'. "
                         f"Available adducts: {list(ADDUCT_MASS_SHIFTS[ionization_mode].keys())}")

    neutral_exact_mass = exact_mass_from_formula(formula = formula)
    expected_mz = neutral_exact_mass + ADDUCT_MASS_SHIFTS[ionization_mode][adduct]

    ion_info = {"formula": formula,
                "neutral_exact_mass": neutral_exact_mass,
                "ionization_mode": ionization_mode,
                "adduct": adduct,
                "expected_mz": expected_mz}

    return ion_info