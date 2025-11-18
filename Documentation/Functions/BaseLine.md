## Description

The `BaseLine` function calculates the baseline of a chromatographic peak by using linear interpolation between baseline points and then subtracts it from the signal.

---
## Key operations

- The function uses linear interpolation to generate a baseline.

---
## Code

```python
from scipy import stats
import numpy as np
def BaseLine(EarlyLoc,LateLoc,Chromatogram,RT_col=2,int_col=5,BaseLinePoints_2=3):
    N_spec=len(Chromatogram[:,0])
    EarlyLoc0=EarlyLoc
    LateLoc0=LateLoc
    EarlyBaseLine=EarlyLoc-BaseLinePoints_2
    if EarlyBaseLine<0:
        EarlyBaseLine=0   
        EarlyLoc+=2
    LateBaseLine=LateLoc+BaseLinePoints_2
    if LateBaseLine>N_spec:
        LateBaseLine=N_spec 
        LateLoc-=2
    EarlyBaseLineMat=Chromatogram[EarlyBaseLine:EarlyLoc,:]
    LateBaseLineMat=Chromatogram[LateLoc:LateBaseLine,:]
    BaseLineMat=np.append(EarlyBaseLineMat,LateBaseLineMat,axis=0)
    X=BaseLineMat[:,RT_col]
    Y=BaseLineMat[:,int_col]
    reg=stats.linregress(X,Y)
    m=reg[0]
    b=reg[1]
    r2=reg[2]**2
    BL=Chromatogram[EarlyLoc0:LateLoc0,2]*m+b    
    return BL

```
---

## Parameters

---

## Input

- [[RT_col]]
- [[LateLoc]]
- [[BaseLinePoints_2]]
- [[Chromatogram]]
- [[EarlyLoc]]
- [[int_col]]

---

## Output

- [[BL]]

---

## Functions


---

## Called by

- [[IntegrateChromatographicPeak]]
- [[PlotChromatogram]]
