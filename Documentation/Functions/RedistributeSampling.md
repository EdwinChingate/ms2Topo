## Description

The `RedistributeSampling` function resamples a chromatographic peak to adjust the density of its data points, using linear interpolation.

---
## Key operations

- The function interpolates the retention time and intensity values to create a new array with a new number of points. If N_new is not provided, it calculates a value based on the length of the input array.

---
## Code

```python
import numpy as np
from scipy.interpolate import interp1d
def RedistributeSampling(PeakChr,N_new=0,RT_col=2,int_col=1):    
    N_signals=len(PeakChr[:,RT_col])
    if N_new==0:
        N_new=2**int(np.ceil(np.log(N_signals)/np.log(2)))
    RedisPeak=np.zeros((N_new,2))
    RT=PeakChr[:,RT_col]
    Int=PeakChr[:,int_col]
    min_RT=np.min(RT)
    max_RT=np.max(RT)
    RT_new=np.linspace(min_RT,max_RT,N_new)
    Int_new=np.interp(RT_new, RT, Int)
    RedisPeak[:,0]=RT_new
    RedisPeak[:,1]=Int_new
    return RedisPeak

```
---

## Parameters

---

## Input

- [[N_new]]
- [[PeakChr]]
- [[RT_col]]
- [[int_col]]

---

## Output

- [[RedisPeak]]

---

## Functions


---

## Called by

- [[SmoothFourier]]
- [[ToolsGaussianChrom]]
