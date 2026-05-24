from __future__ import annotations

import re

def exact_mass_from_formula(formula):
    """
    Calculate the neutral monoisotopic exact mass from a molecular formula.

    Supports simple formulas such as:
        C14H22N2O3
        C10H11N3O3S
        C15H12N2O
    """
    MONOISOTOPIC_MASSES = {"H": 1.00782503223,
                           "C": 12.00000000000,
                           "N": 14.00307400443,
                           "O": 15.99491461957,
                           "P": 30.97376199842,
                           "S": 31.97207117440,
                           "F": 18.99840316273,
                           "Cl": 34.968852682,
                           "Br": 78.9183376,
                           "I": 126.9044719,
                           "Na": 22.9897692820,
                           "K": 38.9637064864}
    formula = formula.strip()
    pattern = r"([A-Z][a-z]?)(\d*)"

    tokens = re.findall(pattern,
                        formula)

    if not tokens:
        raise ValueError(f"Could not parse formula: {formula}")

    reconstructed_formula = "".join(element + count for element, count in tokens)

    if reconstructed_formula != formula:
        raise ValueError("This simple parser only supports formulas without parentheses, "
                         f"isotope labels, or charges. Received: {formula}")

    exact_mass = 0.0

    for element, count in tokens:
        if element not in MONOISOTOPIC_MASSES:
            raise ValueError(f"Element '{element}' is not available in MONOISOTOPIC_MASSES.")

        n_atoms = int(count) if count else 1
        exact_mass = exact_mass + MONOISOTOPIC_MASSES[element] * n_atoms

    return exact_mass