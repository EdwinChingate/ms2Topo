from __future__ import annotations

import numpy as np

def Cosine_2VecSpec(AlignedSpecMat):
    S1_dot_S2 = np.sum(AlignedSpecMat[:, 1] * AlignedSpecMat[:, 2])
    S1_dot_S1 = np.sum(AlignedSpecMat[:, 1] * AlignedSpecMat[:, 1])
    S2_dot_S2 = np.sum(AlignedSpecMat[:, 2] * AlignedSpecMat[:, 2])
    dotXdot = S1_dot_S1 * S2_dot_S2
    if dotXdot == 0:
        return 0
    Cosine = S1_dot_S2 / np.sqrt(dotXdot)
    return Cosine