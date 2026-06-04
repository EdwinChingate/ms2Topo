import numpy as np
def SignalsModulesStats(Modules,SignalVec):
    ModulesStats=[]
    modLoc=0
    for module in Modules:
        Signals=SignalVec[module]
        Signals_mean=np.mean(Signals)
        Signals_std=np.std(Signals)
        Signals_max=np.max(Signals)
        Signals_min=np.min(Signals)
        NSignals=len(module)
        ModulesStats.append([Signals_mean,Signals_std,Signals_max,Signals_min,NSignals,int(modLoc)])
        modLoc+=1
    ModulesStats=np.array(ModulesStats)
    ModulesStats=ModulesStats[ModulesStats[:,2].argsort(),:]
    return ModulesStats
