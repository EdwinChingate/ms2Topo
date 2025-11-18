## Description

`ShowDF` is used to display a Pandas DataFrame as an HTML table. It takes a DataFrame, and optionally a list of column names, and displays the data in a formatted table.

---
## Key operations

- It converts a given input to a Pandas DataFrame if it isn't already, then it uses the `tabulate` library to generate an HTML table of the DataFrame for display.

---
## Code

```python
from IPython.display import HTML, display
import tabulate	
import pandas as pd
def ShowDF(DF,col=''):
    if type(DF)!=type(pd.DataFrame()):
        DF=pd.DataFrame(DF)
    if col=='':
        col=list(DF.columns)
    display(HTML(tabulate.tabulate(DF[col], headers= col,tablefmt='html')))    

```
---

## Parameters

---

## Input

- [[DF]]
- [[col]]

---

## Output


---

## Functions


---

## Called by

- [[ResolvingGaussianChromatogram]]
- [[ShowPop]]
- [[PlotChromatogram]]
