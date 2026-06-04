from CloseNeighboursList import *
from ms2_feat_modules import *
from SignalsModulesStats import *
def LowSignalClustering(SignalVec0,minSignal=0):
    ZeroFil=SignalVec0>0
    SignalVec=SignalVec0[ZeroFil]    
    NeighboursList,SignalsSet=CloseNeighboursList(SignalVec,minSignal=minSignal)
    Modules=ms2_feat_modules(AdjacencyList=NeighboursList,ms2_ids=SignalsSet)
    ModulesStats=SignalsModulesStats(Modules,SignalVec)
    NoiseTresVec=ModulesStats[0,:]
    modLoc=int(NoiseTresVec[-1])
    Module=Modules[modLoc]
    NoiseTresList=[NoiseTresVec,Module]
    return NoiseTresList
