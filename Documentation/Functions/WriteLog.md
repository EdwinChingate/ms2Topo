## Description

`WriteLog` records information about a peak, its relative contribution, and other parameters by calling `ms2Peak_contribution` to calculate the peak contribution, `Parameters_to_string` to format the output, and then appending the formatted string to a log file.

---
## Key operations

- The function uses `ms2Peak_contribution` to calculate the contribution of a peak, and `Parameters_to_string` to convert the parameters to a string. It then writes the string to a log file.

---
## Code

```python
from ms2Peak_contribution import *
from Parameters_to_string import *
def WriteLog(RawSpectrum,Parameters,TotalInt,LogFileName='LogMS2_peaks.csv'):
    mz=Parameters[2]
    mz_std=Parameters[3]
    stdDistance=Parameters[4]    
    relative_contribution=ms2Peak_contribution(RawSpectrum=RawSpectrum,TotalInt=TotalInt,mz=mz,mz_std=mz_std,stdDistance=stdDistance)
    Parameters=relative_contribution+Parameters
    toWrite=Parameters_to_string(Parameters)
    LogFile=open(LogFileName,'a')
    LogFile.write(toWrite)
    LogFile.close()

```
---

## Parameters

---

## Input

- [[TotalInt]]
- [[LogFileName]]
- [[Parameters]]
- [[RawSpectrum]]

---

## Output


---

## Functions

- [[Parameters_to_string]]
- [[ms2Peak_contribution]]

---

## Called by

- [[ms2_peakStats_safe]]
