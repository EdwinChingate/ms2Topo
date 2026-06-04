from close_neighbours_list import *
from ms2_feat_modules import *
from signals_modules_stats import *
def low_signal_clustering(SignalVec0,minSignal=0):
    ZeroFil=SignalVec0>0
    SignalVec=SignalVec0[ZeroFil]    
    NeighboursList,SignalsSet=close_neighbours_list(SignalVec,minSignal=minSignal)
    Modules=ms2_feat_modules(AdjacencyList=NeighboursList,ms2_ids=SignalsSet)
    ModulesStats=signals_modules_stats(Modules,SignalVec)
    NoiseTresVec=ModulesStats[0,:]
    modLoc=int(NoiseTresVec[-1])
    Module=Modules[modLoc]
    NoiseTresList=[NoiseTresVec,Module]
    return NoiseTresList
