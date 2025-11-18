## Description

The `SamplesNames_from_List` function loads sample information from an excel file specified by the `SamplesInfName` variable, and returns it as a pandas DataFrame.

---
## Key operations

- The function reads an excel file specified by `SamplesInfName` using pandas.
- It returns the DataFrame created from the excel file, `SamplesInfDF`.

---
## Code

```python
import pandas as pd
def SamplesNames_from_List(SamplesInfName):
    SamplesInfDF=pd.read_excel(SamplesInfName,index_col=0)
    return SamplesInfDF

```
---

## Parameters

---

## Input

- [[SamplesInfName]]

---

## Output

- [[SamplesInfDF]]

---

## Functions


---

## Called by

