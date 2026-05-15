from __future__ import annotations

import numpy as np

def FlatMatrix_woDiag(matrix,
                      n):
    FlatMatrix = []
    for row in np.arange(n):
        for col in np.arange(n):
            if row != col:
                FlatMatrix.append(matrix[row,col])
    return FlatMatrix