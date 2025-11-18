## Description

The `PlotSpec` function plots the raw spectrum data, including options for axis limits and display control.

---
## Key operations

- The function plots the m/z values against the intensity values. It also sets the axis limits, based on the input values, and then it displays the generated plot of the raw spectrum if `show` is `True`.

---
## Code

```python
import matplotlib.pyplot as plt
def PlotSpec(RawSpectrum,xlim=[],ylim=[],show=True):
    if len(xlim)>0:
        plt.xlim(xlim)
    if len(ylim)>0:
        plt.ylim(ylim)
    plt.plot(RawSpectrum[:,0],RawSpectrum[:,1],'.')
    if show:
        plt.show()

```
---

## Parameters

---

## Input

- [[show]]
- [[xlim]]
- [[RawSpectrum]]
- [[ylim]]

---

## Output


---

## Functions


---

## Called by

