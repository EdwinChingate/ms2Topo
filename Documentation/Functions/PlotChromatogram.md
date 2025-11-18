## Description

The `PlotChromatogram` function extracts, refines, and visualizes a chromatogram, displaying both the raw data and the processed peaks, along with a table with peak information.

---
## Key operations

- The function calls `MaxIntChromatogram` to extract the chromatogram, then calls `Feat_RT_edges` to refine the chromatographic peaks. The function then generates a plot of the raw chromatogram data and the smoothed and baseline-corrected peaks, it also displays a DataFrame of the detected peaks and their features.

---
## Code

```python
from MaxIntChromatogram import *
from Feat_RT_edges import *
from BaseLine import *
from ShowDF import *
import matplotlib.pyplot as plt
def PlotChromatogram(mz,mz_std,DataSet,DataSetName,MS1IDVec,AllPeaks,minIntFrac=1,int_col=1,RT_col=2,BaseLinePoints_2=3,LogFileName='LogFile_ms1.csv',stdDistance=1,minSignals=5,MaxCount=3,minInt=1e3,Points_for_regression=4,alpha=0.01,minSpec=10,minWindow=11,minPoly=5):
    Chromatogram=MaxIntChromatogram(mz=mz,mz_std=mz_std,AllPeaks=AllPeaks,stdDistance=stdDistance)    
    Chromatogram=Chromatogram[Chromatogram[:,RT_col].argsort(),:].copy()
    ChrMat=Feat_RT_edges(Chromatogram=Chromatogram,minSpec=minSpec,int_col=int_col,stdDistance=3,NoiseCluster=False)
    plt.plot(Chromatogram[:,2],Chromatogram[:,1],'.')
    plt.show()
    ShowDF(ChrMat)
    if len(ChrMat)==0:
        return []
    min_mz=mz-mz_std*stdDistance
    max_mz=mz+mz_std*stdDistance
    SummarizeChFeat=[]
    for sig in ChrMat:
        EarlyLoc=int(sig[0])
        LateLoc=int(sig[1])
        PeakChr=Chromatogram[EarlyLoc:LateLoc,:]    
        NSpec=len(PeakChr[:,0])
        wl=min([int(NSpec/4)*2+1,minWindow])
        poly=min([int(wl/2),minPoly])    
        SoftInt=savgol_filter(PeakChr[:,int_col], wl, poly)
        BL=BaseLine(EarlyLoc=EarlyLoc,LateLoc=LateLoc,Chromatogram=Chromatogram,RT_col=RT_col,int_col=int_col,BaseLinePoints_2=BaseLinePoints_2)
        No_NoiseSignal=SoftInt-BL
        plt.plot(PeakChr[:,2],PeakChr[:,1],'.')
        plt.plot(PeakChr[:,2],SoftInt,'-')
        plt.plot(PeakChr[:,2],BL,'-')
        plt.show()
        maxInt=np.max(No_NoiseSignal)
        minInt=minIntFrac*maxInt/100
        PosLoc=np.where(No_NoiseSignal>minInt)[0]
        if len(PosLoc)<4:
            return 0
        No_NoiseSignal=No_NoiseSignal[PosLoc]
        X=PeakChr[PosLoc,RT_col]
        Y=No_NoiseSignal
        plt.plot(X,Y,'-')
        plt.show()
    return Chromatogram

```
---

## Parameters

---

## Input

- [[AllPeaks]]
- [[DataSetName]]
- [[mz]]
- [[Points_for_regression]]
- [[stdDistance]]
- [[MaxCount]]
- [[LogFileName]]
- [[MS1IDVec]]
- [[RT_col]]
- [[minWindow]]
- [[BaseLinePoints_2]]
- [[DataSet]]
- [[alpha]]
- [[minInt]]
- [[minSpec]]
- [[minIntFrac]]
- [[int_col]]
- [[minPoly]]
- [[mz_std]]
- [[minSignals]]

---

## Output

- [[]]
- [[Chromatogram]]
- [[0]]

---

## Functions

- [[BaseLine]]
- [[ShowDF]]
- [[MaxIntChromatogram]]
- [[Feat_RT_edges]]

---

## Called by

