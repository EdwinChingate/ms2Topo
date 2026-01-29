import numpy as np
def Update_ids_FeatureModules(Feature_module,
                              Feature_Modules):    
    npFeature_module = np.array(Feature_module, dtype = 'int')
    Modules=[]
    for module in Feature_Modules:
        feature_module = list(npFeature_module[module])
        Modules.append(feature_module)
    return Modules
