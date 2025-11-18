## Description

The `IntegrateChromatographicPeak` function calculates the integrated intensity (`I`) of a chromatographic peak by first smoothing the data, then subtracting a baseline (`BaseLine`), and integrating the resulting signal above a minimum intensity threshold (`minIntFrac`), using the indices `EarlyLoc` and `LateLoc` on the `Chromatogram`.

---
## Key operations

- It extracts the peak region from the `Chromatogram` using `EarlyLoc` and `LateLoc`, applies Savitzky-Golay smoothingto the intensity data, and performs baseline correctionusing the `BaseLine` function. It then integrates the baseline-corrected intensity to calculate the peak area, I. The function removes any signal below a minimum intensity fraction defined by `minIntFrac`.

---
## Code

```python
from scipy import integrate	
from scipy.signal import savgol_filter
from BaseLine import *
def IntegrateChromatographicPeak(EarlyLoc,LateLoc,Chromatogram,minIntFrac=1,RT_col=2,int_col=5,BaseLinePoints_2=3,minWindow=11,minPoly=5):
    PeakChr=Chromatogram[EarlyLoc:LateLoc,:]    
    NSpec=len(PeakChr[:,0])
    wl=min([int(NSpec/4)*2+1,minWindow])
    poly=min([int(wl/2),minPoly])    
    SoftInt=savgol_filter(PeakChr[:,int_col], wl, poly)    
    BL=BaseLine(EarlyLoc=EarlyLoc,LateLoc=LateLoc,Chromatogram=Chromatogram,RT_col=RT_col,int_col=int_col,BaseLinePoints_2=BaseLinePoints_2)
    No_NoiseSignal=SoftInt-BL    
    #plt.plot(PeakChr[:,2],PeakChr[:,1],'.')
    #plt.plot(PeakChr[:,2],SoftInt,'-')
    #plt.plot(PeakChr[:,2],BL,'-')
    #plt.show()
    maxInt=np.max(No_NoiseSignal)
    minInt=minIntFrac*maxInt/100
    PosLoc=np.where(No_NoiseSignal>minInt)[0]
    if len(PosLoc)<4:
        return 0
    No_NoiseSignal=No_NoiseSignal[PosLoc]
    X=PeakChr[PosLoc,RT_col]
    Y=No_NoiseSignal
    #plt.plot(X,Y,'-')
    #plt.show()
    I=integrate.simpson(y=Y,x=X)   
    return I

```
---

## Parameters

---

## Input

- [[RT_col]]
- [[minWindow]]
- [[LateLoc]]
- [[BaseLinePoints_2]]
- [[Chromatogram]]
- [[EarlyLoc]]
- [[minIntFrac]]
- [[int_col]]
- [[minPoly]]

---

## Output

- [[I]]
- [[0]]

---

## Functions

- [[BaseLine]]

---

## Called by

- [[SummarizeChPeak]]
- [[Summarize_ms1_ChPeak]]
