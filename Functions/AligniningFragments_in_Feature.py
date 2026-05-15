from __future__ import annotations

import numpy as np

def AligniningFragments_in_Feature(Frag_Modules,
                                   All_ms2,
                                   N_features):
    N_Fragments = len(Frag_Modules)
    AlignedFragmentsMat = np.zeros((N_Fragments,
                                    N_features + 1))
    AlignedFragments_mz_Mat = np.zeros((N_Fragments,
                                        N_features + 1))
    for fragment_id in np.arange(N_Fragments,
                                 dtype = 'int'):
        Fragment_module = Frag_Modules[fragment_id]
        FragmentTable = All_ms2[Fragment_module, :]
        AlignedFragmentsMat[fragment_id, 0] = np.mean(FragmentTable[:, 0])
        AlignedFragments_mz_Mat[fragment_id, 0] = np.mean(FragmentTable[:, 0])
        Fragments_ids = np.array(FragmentTable[:, 10],
                                 dtype = 'int')
        AlignedFragmentsMat_loc = Fragments_ids + 1
        AlignedFragmentsMat[fragment_id, AlignedFragmentsMat_loc] = FragmentTable[:, 9]
        AlignedFragments_mz_Mat[fragment_id, AlignedFragmentsMat_loc] = FragmentTable[:, 0]
    FragmentsOrder = AlignedFragmentsMat[:, 0].argsort()
    AlignedFragmentsMat = AlignedFragmentsMat[FragmentsOrder]
    AlignedFragments_mz_Mat = AlignedFragments_mz_Mat[FragmentsOrder]
    return [AlignedFragmentsMat, AlignedFragments_mz_Mat]