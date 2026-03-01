import numpy as np
def FeatureModuleStats(All_FeaturesTable,
                       module,
                       SamplesNames,
                       IntramoduleCosineStatsVec,
                       feature_id,
                       sampling_samples = 0,
                       percentile_mz = 5,
                       percentile_RT = 5):
    FeatureTable = All_FeaturesTable[module, :]
    N_samples = len(SamplesNames)
    AlignedSamplesVec = np.zeros((N_samples + 18))
    Samples_ids = np.array(FeatureTable[:, 6],
                           dtype = 'int')
    Samples_ids = set(list(Samples_ids))
    Samples_ids = np.array(list(Samples_ids))
    AlignedSamplesVec_loc = Samples_ids + 18
    AlignedSamplesVec[AlignedSamplesVec_loc] = 1    
    mz = np.median(FeatureTable[:, 1])
    AlignedSamplesVec[0] = mz
    AlignedSamplesVec[1] = np.percentile(FeatureTable[:, 1],
                                         percentile_mz)
    AlignedSamplesVec[2] = np.percentile(FeatureTable[:, 1],
                                         100 - percentile_mz)
    Q1_mz = np.percentile(FeatureTable[:, 1],
                          25)
    Q3_mz = np.percentile(FeatureTable[:, 1],
                          75)     
    IQR_mz = Q3_mz - Q1_mz    
    AlignedSamplesVec[3] = IQR_mz / mz * 1e6
    AlignedSamplesVec[4] = sampling_samples
    AlignedSamplesVec[5] = len(Samples_ids)
    AlignedSamplesVec[6] = len(module)
    AlignedSamplesVec[7: 12] = IntramoduleCosineStatsVec
    AlignedSamplesVec[12] = np.median(FeatureTable[:, 2])
    AlignedSamplesVec[13] = np.percentile(FeatureTable[:, 2],
                                          25)
    AlignedSamplesVec[14] = np.percentile(FeatureTable[:, 2],
                                          75)  
    AlignedSamplesVec[15] = np.percentile(FeatureTable[:, 2],
                                          percentile_RT)
    AlignedSamplesVec[16] = np.percentile(FeatureTable[:, 2],
                                          100 - percentile_RT)    
    AlignedSamplesVec[17] =int(feature_id)    
    return AlignedSamplesVec
