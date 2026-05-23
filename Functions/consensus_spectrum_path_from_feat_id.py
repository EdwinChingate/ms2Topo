from __future__ import annotations

from pathlib import Path
from clean_feat_id import *

def consensus_spectrum_path_from_feat_id(consensus_spectra_folder,
                                         feat_id,
                                         file_name_template = "Consensus_ms2-spectra_{feat_id}.csv"):
    """
    Build the path to a saved ms2Topo consensus MS2 spectrum.
    """

    feat_id = clean_feat_id(feat_id)
    consensus_spectra_folder = Path(consensus_spectra_folder)

    consensus_spectrum_path = consensus_spectra_folder / file_name_template.format(feat_id = feat_id)

    return consensus_spectrum_path