## Description

`AdjustingPeaksContributions` calculates the contribution of each Gaussian peak to the overall signal, using a least squares method to adjust the peak contributions, which results in a vector of coefficients to refine peak parameters.

---
## Key operations

- It takes a chromatogram and a matrix of overlapping Gaussian peaks, calculates the contributions of each peak to the overall signal, and uses a linear algebra method to solve for the coefficients. It uses matrix multiplication to calculate the contributions of each peak.

---
## Code

```python
import numpy as np
def AdjustingPeaksContributions(smooth_peaks,ChromatogramMatrix):
    IntVec=smooth_peaks[:,1]
    NPeaks=len(ChromatogramMatrix[0,:])
    ChromatogramMatrixTranspose=ChromatogramMatrix.T
    MatrixTransInt=np.matmul(ChromatogramMatrixTranspose,IntVec)
    MatrixTransChromMat=np.matmul(ChromatogramMatrixTranspose,ChromatogramMatrix)
    while True:
        try:
            InvMatrixTransChromMat=np.linalg.inv(MatrixTransChromMat)
            ContributionsVec=np.matmul(InvMatrixTransChromMat,MatrixTransInt)
            break
        except:
            ContributionsVec=np.ones(NPeaks)
            break
    return ContributionsVec

```
---

## Parameters

---

## Input

- [[ChromatogramMatrix]]
- [[smooth_peaks]]

---

## Output

- [[ContributionsVec]]

---

## Functions


---

## Called by

- [[first_round_chromatogram_deconvolution]]
- [[RefineChromPeak]]
- [[RefineParameters]]
