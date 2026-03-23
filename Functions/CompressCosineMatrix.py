from __future__ import annotations
import numpy as np
def CompressCosineMatrix(Modules,
                         CosineMat,
                         percentile = 10):
    
    N_modules = len(Modules)
    CompactCosineTen = np.zeros((N_modules,
                                 N_modules,
                                 3))
    
    for module_idA in np.arange(N_modules):
        moduleA = list(Modules[module_idA])
        for module_idB in np.arange(module_idA + 1,
                                    N_modules):
            moduleB = list(Modules[module_idB])
            CompactCosineTen[module_idA, module_idB, 1] = np.median(CosineMat[np.ix_(moduleA,
                                                                                     moduleB)])
            CompactCosineTen[module_idB, module_idA, 1] = CompactCosineTen[module_idA, module_idB, 1]
            CompactCosineTen[module_idA, module_idB, 2] = np.percentile(CosineMat[np.ix_(moduleA,
                                                                                         moduleB)],
                                                                        100-percentile)
            CompactCosineTen[module_idB, module_idA, 2] = CompactCosineTen[module_idA,module_idB,2]
            CompactCosineTen[module_idA, module_idB, 0] = np.percentile(CosineMat[np.ix_(moduleA,
                                                                                         moduleB)],
                                                                        percentile)
            CompactCosineTen[module_idB, module_idA, 0] = CompactCosineTen[module_idA,module_idB,0]  
            
    return CompactCosineTen
