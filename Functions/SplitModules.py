import numpy as np
def SplitModules(Feature_module,
                 feature_module,
                 ConflictiveNodes):
    Modules = [np.array(Feature_module)[feature_module].tolist()]
    for conflictive_node in ConflictiveNodes:
        Modules.append([int(Feature_module[conflictive_node])])
    return Modules
