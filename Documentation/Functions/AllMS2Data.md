## Description

`AllMS2Data` extracts and filters MS2 spectra based on m/z and RT ranges, using `mz_RT_spectrum_filter` to process the data and output the extracted spectra in the `SummMS2` variable.

---
## Key operations

- It iterates through the spectra in the dataset, filters them based on the provided RT and m/zranges and it uses the `mz_RT_spectrum_filter` function to perform the filtering and extraction.

---
## Code

```python
import numpy as np
from mz_RT_spectrum_filter import *
def AllMS2Data(DataSet,min_RT=0,max_RT=1e5,min_mz=0,max_mz=1e4):
    SummMS2=[]
    FirstSpec=True
    spectrum_id=0
    for SpectralSignals in DataSet:
        SummMS2=mz_RT_spectrum_filter(SpectralSignals=SpectralSignals,SummMS2=SummMS2,min_RT=min_RT,max_RT=max_RT,min_mz=min_mz,max_mz=max_mz,spectrum_id=spectrum_id)
        spectrum_id+=1
    SummMS2=np.array(SummMS2)      
    SummMS2=SummMS2[SummMS2[:,0].argsort(),:]
    return SummMS2

```
---

## Parameters

---

## Input

- [[max_RT]]
- [[DataSet]]
- [[min_mz]]
- [[max_mz]]
- [[min_RT]]

---

## Output

- [[SummMS2]]

---

## Functions

- [[mz_RT_spectrum_filter]]

---

## Called by

