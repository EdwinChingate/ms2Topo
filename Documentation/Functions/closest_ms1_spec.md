## Description

`closest_ms1_spec` identifies the closest MS1 spectra to a given MS2 spectrum, based on the retention time and the `MS2_to_MS1_ratio`, returning their identifiers.

---
## Key operations

- The function calculates the retention time differences between the given MS2 spectrum and all MS1 spectra, using `MS1IDVec`. It then selects the closest MS1 spectra based on the provided `MS2_to_MS1_ratio`, and returns their IDs.

---
## Code

```python
import numpy as np
def closest_ms1_spec(mz,RT,MS2_Fullsignal_id,SummMS2,MS1IDVec,MS2_to_MS1_ratio=10):    
    ID_filter=(MS1IDVec[:,0]<MS2_Fullsignal_id)&(MS1IDVec[:,0]>(MS2_Fullsignal_id-MS2_to_MS1_ratio)) #The MS2 is generated with the ions from the MS1, so the MS2 RT and id, would be higher
    Earlier_MS1IDVec=MS1IDVec[ID_filter,:]
    RT_DifVec=RT-Earlier_MS1IDVec[:,1]
    Min_RT_Dif=np.min(RT_DifVec)
    Closest_MS1_Loc=np.where(RT_DifVec==Min_RT_Dif)[0]
    spectrum_idVec=Earlier_MS1IDVec[RT_DifVec.argsort(),0]
    return spectrum_idVec

```
---

## Parameters

---

## Input

- [[SummMS2]]
- [[RT]]
- [[mz]]
- [[MS1IDVec]]
- [[MS2_to_MS1_ratio]]
- [[MS2_Fullsignal_id]]

---

## Output

- [[spectrum_idVec]]

---

## Functions


---

## Called by

- [[ms2_features_stats]]
