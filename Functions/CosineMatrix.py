import numpy as np
from Cosine_2VecSpec import *
def CosineMatrix(AlignedFragmentsMat,
                 N_features):
    CosineMat = np.zeros((N_features,N_features))
    for feature_id1 in np.arange(N_features-1,dtype='int'):
        for feature_id2 in np.arange(feature_id1+1,N_features,dtype='int'):
            AlignedSpecMat = AlignedFragmentsMat[:,[0,feature_id1+1,feature_id2+1]]
            Cosine = Cosine_2VecSpec(AlignedSpecMat = AlignedSpecMat)
            CosineMat[feature_id1,feature_id2] = Cosine
            CosineMat[feature_id2,feature_id1] = Cosine
    return CosineMat
