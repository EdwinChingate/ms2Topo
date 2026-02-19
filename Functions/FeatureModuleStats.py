import numpy as np
from ttest import *
def FeatureModuleStats(All_FeaturesTable,
                       module,
                       SamplesNames,
                       feature_id):
    FeatureTable = All_FeaturesTable[module, :]
    N_samples = len(SamplesNames)
    AlignedSamplesVec = np.zeros((N_samples+12))
    AlignedSamplesVec[0] = np.mean(FeatureTable[:, 1])
    AlignedSamplesVec[1] = np.std(FeatureTable[:, 1])
    AlignedSamplesVec[2] = len(module)
    AlignedSamplesVec[3] = 0
    AlignedSamplesVec[4] = 0
    AlignedSamplesVec[6] = 0
    AlignedSamplesVec[7] = 0
    AlignedSamplesVec[8] = np.mean(FeatureTable[:, 2])
    AlignedSamplesVec[9] = np.min(FeatureTable[:, 2])
    AlignedSamplesVec[10] =np.max(FeatureTable[:, 2])
    AlignedSamplesVec[11] =int(feature_id)
    Samples_ids = np.array(FeatureTable[:, 6],
                           dtype = 'int')
    Samples_ids = set(list(Samples_ids))
    Samples_ids = np.array(list(Samples_ids))
    AlignedSamplesVec_loc = Samples_ids + 12
    AlignedSamplesVec[AlignedSamplesVec_loc] = 1
    return AlignedSamplesVec
