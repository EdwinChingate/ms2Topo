## Description

The `ListStats` function calculates the mean, `Data_mean`, the standard deviation, `Data_std`, and the difference between them for a given list of numerical data, `DataList`.

---
## Key operations

- It calculates the mean (`Data_mean`) and standard deviation (`Data_std`) of the input `DataList`. It also calculates the difference between the mean and the standard deviation.

---
## Code

```python
import numpy as np
def ListStats(DataList):
    Data_mean=np.mean(DataList)
    Data_std=np.std(DataList)
    return [Data_mean,Data_std,Data_mean-Data_std]

```
---

## Parameters

---

## Input

- [[DataList]]

---

## Output

- [[Data_std]]
- [[Data_mean]]
- [[Data_mean-Data_std]]

---

## Functions


---

## Called by

