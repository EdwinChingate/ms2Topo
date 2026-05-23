from __future__ import annotations

def get_precursor_mz(spectrum):
    precursors = spectrum.getPrecursors()

    if len(precursors) == 0:
        return None

    return precursors[0].getMZ()