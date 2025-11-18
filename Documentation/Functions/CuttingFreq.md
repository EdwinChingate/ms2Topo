## Description

The `CuttingFreq` function calculates a minimum threshold frequency value based on input signal frequencies and a low signal clustering, used to filter out noise.

---
## Key operations

- The function first uses `LowSignalClustering` to identify the noise frequencies. It then calculates a threshold based on the results of the clustering.

---
## Code

```python
import numpy as np
from LowSignalClustering import *
def CuttingFreq(fft_signal,frequencies,stdDistance=1,MinSignalFraction=0.5):
    NSig=len(fft_signal)
    NoiseTresVec=LowSignalClustering(SignalVec0=np.abs(fft_signal))[0]
    NoiseTres=NoiseTresVec[2]    
    NoiseLoc=fft_signal<=NoiseTres
    NoiseFreq=frequencies[NoiseLoc]
    Freq_mean=np.mean(abs(NoiseFreq))
    Freq_std=np.std(abs(NoiseFreq))
    FreqTres=Freq_mean-Freq_std*stdDistance
    MinSignalNumber=int(NSig*MinSignalFraction)
    FreqVec=np.abs(frequencies[np.abs(frequencies).argsort()].copy())
    MinFreqTres=FreqVec[MinSignalNumber] 
    FreqTres=np.max([FreqTres,MinFreqTres])
    return FreqTres

```
---

## Parameters

---

## Input

- [[frequencies]]
- [[stdDistance]]
- [[fft_signal]]
- [[MinSignalFraction]]

---

## Output

- [[FreqTres]]

---

## Functions

- [[LowSignalClustering]]

---

## Called by

- [[SmoothFourier]]
