import numpy as np
from ttest import *
def ms2GaussFeatStats(All_SummMS2Table,
                      SamplesNames,
                      Modules,
                      min_ms2_spectra = 4):
    N_samples = len(SamplesNames)
    N_Features = len(Modules)
    AlignedSamplesMat = np.zeros((N_Features,N_samples+10))
    ms2_ids_inModules = []
    for feature_id in np.arange(N_Features,dtype = 'int'):
        Feature_module = Modules[feature_id]
        FeatureTable = All_SummMS2Table[Feature_module,:]
        AlignedSamplesMat[feature_id,0] = np.mean(FeatureTable[:,1])
        AlignedSamplesMat[feature_id,1] = np.std(FeatureTable[:,1])
        AlignedSamplesMat[feature_id,2] = len(Feature_module)
        AlignedSamplesMat[feature_id,6] = np.mean(FeatureTable[:,2])
        AlignedSamplesMat[feature_id,7] = np.min(FeatureTable[:,2])
        AlignedSamplesMat[feature_id,8] = np.max(FeatureTable[:,2])
        AlignedSamplesMat[feature_id,9] = int(feature_id)
        ms2_ids_inModules.append(FeatureTable[:,[0,6]])
        Samples_ids = np.array(FeatureTable[:,6],dtype = 'int')
        Samples_ids = set(list(Samples_ids))
        Samples_ids = np.array(list(Samples_ids))
        AlignedSamplesMat_loc = Samples_ids+10
        AlignedSamplesMat[feature_id,AlignedSamplesMat_loc] = 1
    SpectralFilter = np.where(AlignedSamplesMat[:,2]>min_ms2_spectra)[0]
    AlignedSamplesMat = AlignedSamplesMat[SpectralFilter,:] 
    NSamplesVec = list(AlignedSamplesMat[:,2])
    t_refVec = list(map(ttest,NSamplesVec))    
    AlignedSamplesMat[:,4] = t_refVec*AlignedSamplesMat[:,1]/np.sqrt(NSamplesVec)
    AlignedSamplesMat[:,5] = AlignedSamplesMat[:,4]/AlignedSamplesMat[:,0]*1e6    
    AlignedSamplesMat = AlignedSamplesMat[AlignedSamplesMat[:,0].argsort()]    
    return [AlignedSamplesMat,ms2_ids_inModules]
