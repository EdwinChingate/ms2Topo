import numpy as np
def CloseNeighboursList(SignalVec,minSignal=0):
    if minSignal==0:
        minSignal=np.min(SignalVec)
    NeighboursList=[]
    NSignals=len(SignalVec)
    SignalsSet=set(np.arange(NSignals,dtype='int'))
    for signal_id in SignalsSet:
        signal=SignalVec[signal_id]
        DifSignalVec=np.abs(SignalVec-signal)
        NeighboursLoc=np.where(DifSignalVec<minSignal)[0]
        NeighboursList.append(NeighboursLoc)
    return [NeighboursList,SignalsSet]
