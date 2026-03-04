from __future__ import annotations
import numpy as np
def FillAlignedFragmentsSamplesSpectraMat(AlignedFragmentsMat,  # ← FIXED: non-default before default
                                          All_ms2,              # ← FIXED: non-default before default
                                          SamplesSamplesList,   # ← ADDED: needed for matrix sizing
                                          std_distance = 3,
                                          ppm_tol = 20):
    
    mz_FragmentsVec = AlignedFragmentsMat[:, 0]
    N_Fragments = len(mz_FragmentsVec)

    AlignedFragmentsSamplesSpectraMat = np.zeros((N_Fragments,
                                                  len(SamplesSamplesList) + 1))  # ← FIXED: was Spectra_idVec (undefined here)
    AlignedFragmentsSamplesSpectraMat[:, 0] = AlignedFragmentsMat[:, 0]

    mzVec = All_ms2[:, 0]
    mz_stdVec = All_ms2[:, 1]
    mz_std_edgeVec = np.minimum(mz_stdVec * std_distance,
                                ppm_tol / 1e6 * mzVec)
    mzMaxVec = mzVec + mz_std_edgeVec
    mzMinVec = mzVec - mz_std_edgeVec

    for fragment_id in np.arange(N_Fragments):
        mz = mz_FragmentsVec[fragment_id]
        mzLoc = np.where((mzMinVec < mz) & (mzMaxVec > mz))[0]
        Fragments_in_line = np.array(All_ms2[mzLoc, 10], dtype = 'int')
        AlignedFragmentsSamplesSpectraMat[fragment_id, Fragments_in_line + 1] = All_ms2[mzLoc, 9]

    return AlignedFragmentsSamplesSpectraMat
