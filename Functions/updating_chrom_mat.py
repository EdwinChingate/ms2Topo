import numpy as np
def updating_chrom_mat(ChromatogramMatrix,ContributionsVec):
    Updated_ChromatogramMatrix=ChromatogramMatrix.copy()
    NContributions=len(ContributionsVec)
    for peak_id in np.arange(NContributions,dtype='int'):
        Updated_ChromatogramMatrix[:,peak_id]=ChromatogramMatrix[:,peak_id]*ContributionsVec[peak_id]
    return Updated_ChromatogramMatrix
