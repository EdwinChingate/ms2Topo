## Description

The `Feat_RT_edges` function identifies the start and end points of chromatographic peaks by removing noise from the chromatogram using a low signal clustering or a distance distribution method.

---
## Key operations

- It uses either `LowSignalClustering` or `DistanceDistribution` to identify noise, then it filters the chromatogram based on this noise threshold.

---
## Code

```python
import numpy as np
from LowSignalClustering import *
from DistanceDistribution import *
from ResolvingChromatogram import *
def Feat_RT_edges(Chromatogram,minSpec=10,stdDistance=3,int_col=5,NoiseCluster=False):    
    if NoiseCluster:
        NoiseTresVec=LowSignalClustering(SignalVec0=Chromatogram[:,int_col])[0]
    else:
        Module=LowSignalClustering(SignalVec0=Chromatogram[:,int_col])[1]
        NoiseTresVec=DistanceDistribution(SignalVec0=Chromatogram[Module,int_col])
    NoiseTres=NoiseTresVec[0]+NoiseTresVec[1]*stdDistance
    #print(NoiseTres)
    #plt.plot(Chromatogram[:,2],Chromatogram[:,1],'k.')
    #plt.plot(Chromatogram[:,2][[0,-1]],[NoiseTres,NoiseTres])
    #plt.show()
    IntVec=Chromatogram[:,int_col]
    ValidSignalsLoc=np.where(IntVec>NoiseTres)[0]
    if len(ValidSignalsLoc)==0:
        return []
    ValidSignalsLoc_Future=ValidSignalsLoc[1:]
    ValidSignalsLoc_Past=ValidSignalsLoc[:-1]
    LocDisVec=ValidSignalsLoc_Future-ValidSignalsLoc_Past
    ValidSignalsTresLoc=np.where(LocDisVec>1)[0]
    N_Clusters=len(ValidSignalsTresLoc)+1
    ClustersMat=np.zeros((N_Clusters,3))
    ClustersMat[1:,0]=ValidSignalsLoc_Future[ValidSignalsTresLoc]
    ClustersMat[:-1,1]=ValidSignalsLoc_Past[ValidSignalsTresLoc]+1
    ClustersMat[0,0]=np.min(ValidSignalsLoc)
    ClustersMat[-1,1]=np.max(ValidSignalsLoc)
    ClustersMat[:,2]=ClustersMat[:,1]-ClustersMat[:,0]
    MinSpecFil=ClustersMat[:,2]>minSpec
    NoNoiseClusters=ClustersMat[MinSpecFil,:]
    if len(NoNoiseClusters)==0:
        return []
    FirstChPeak=True
    for no_noise in NoNoiseClusters:
        EarlyLoc=int(no_noise[0])
        LateLoc=int(no_noise[1])
        ChrMat=ResolvingChromatogram(EarlyLoc=EarlyLoc,LateLoc=LateLoc,Chromatogram=Chromatogram,minSpec=minSpec,int_col=int_col)
        if FirstChPeak:
            ChrPeakMat=ChrMat
            FirstChPeak=False
        else:
            ChrPeakMat=np.append(ChrPeakMat,ChrMat,axis=0)    
    return ChrPeakMat

```
---

## Parameters

---

## Input

- [[stdDistance]]
- [[NoiseCluster]]
- [[Chromatogram]]
- [[minSpec]]
- [[int_col]]

---

## Output

- [[]]
- [[ChrPeakMat]]

---

## Functions

- [[DistanceDistribution]]
- [[ResolvingChromatogram]]
- [[LowSignalClustering]]

---

## Called by

- [[Chrom_ms1Peaks_Summaries]]
- [[PlotChromatogram]]
- [[ModuleChromSummaries]]
