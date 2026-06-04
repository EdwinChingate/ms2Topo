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
