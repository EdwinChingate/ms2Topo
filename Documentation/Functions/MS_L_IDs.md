## Description

The `MS_L_IDs` function retrieves a subset of data from `DataSet` based on the provided list of identifiers `IDvec`, and the retention time ranges (`min_RT` and `max_RT`).

---
## Key operations

- It filters the dataset based on a list of identifiers present in `IDvec`, selecting the corresponding data entries. It also filters the data based on the retention time values provided by `min_RT` and `max_RT`.

---
## Code

```python
import numpy as np
def MS_L_IDs(DataSet,min_RT=0,max_RT=1e5,RT_tol=10,Level=1):
    IDvec=[]
    spectrum_id=0
    min_RT=min_RT-RT_tol
    max_RT=max_RT+RT_tol
    for SpectralSignals in DataSet:
        MSLevel=SpectralSignals.getMSLevel()
        RT=SpectralSignals.getRT()
        if MSLevel==Level and RT>min_RT:            
            IDvec.append([int(spectrum_id),RT])
        if RT>max_RT:
            break
        spectrum_id+=1
    IDvec=np.array(IDvec)
    return IDvec

```
---

## Parameters

---

## Input

- [[max_RT]]
- [[Level]]
- [[DataSet]]
- [[min_RT]]
- [[RT_tol]]

---

## Output

- [[IDvec]]

---

## Functions


---

## Called by

- [[RefineFeaturesTable_withChromatogram]]
