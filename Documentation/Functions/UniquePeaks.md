## Description

`UniquePeaks` filters out peaks based on intensity and then iterates through a list of peaks, combining those that are too similar based on the `PeakTol` parameter, and adding them to the `UniqueParametersMat` array..

---
## Key operations

- The function filters peaks based on their integral values, then iterates through the remaining peaks, comparing each to the previous one. If the difference between two peaks is within the tolerance, the function decides whether to keep both peaks or to combine their information based on the `KeepAllPeaks` parameter.

---
## Code

```python
import numpy as np
def UniquePeaks(ParametersMat,PeakTol=[0.1,0.01,1e3],KeepAllPeaks=False,boundsMat=[]):    
    minIntLoc=ParametersMat[:,2]>PeakTol[2]
    ParametersMat=ParametersMat[minIntLoc,:]
    NPeaks=len(ParametersMat[:,0])
    UniqueParametersMat=(ParametersMat[0,:].copy()).reshape(1,-1)  
    EarlierPeak=ParametersMat[0,:].copy()
    for peak_id in np.arange(1,NPeaks):        
        Peak=(ParametersMat[peak_id,:].copy()).reshape(1,-1)  
        PeakDif=Peak-EarlierPeak        
        EvalPeakDif=np.where((PeakDif-PeakTol)<0)[0]
        if len(EvalPeakDif)<3:
            UniqueParametersMat=np.append(UniqueParametersMat,Peak,axis=0)
            EarlierPeak=Peak
        elif KeepAllPeaks:
            UniqueParametersMat=np.append(UniqueParametersMat,Peak,axis=0)
            UniqueParametersMat[-1,2]=UniqueParametersMat[-1,2].copy()+UniqueParametersMat[-2,2].copy()
            UniqueParametersMat[-1,2]=0
            UniqueParametersMat[-1,0]=boundsMat[0,0]
            EarlierPeak=Peak
    return UniqueParametersMat

```
---

## Parameters

---

## Input

- [[PeakTol]]
- [[KeepAllPeaks]]
- [[ParametersMat]]
- [[0.01]]
- [[boundsMat]]
- [[1e3]]

---

## Output

- [[UniqueParametersMat]]

---

## Functions


---

## Called by

- [[Mate_square_WildPop]]
