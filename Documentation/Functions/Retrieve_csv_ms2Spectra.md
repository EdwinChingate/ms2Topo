## Description

The `Retrieve_csv_ms2Spectra` function loads MS2 spectra from CSV files. It uses `SummaryFile` and `ms2Folder` to locate the files, and uses `SFindicator` to find the spectrum ids, saving all of the spectra to `SpectraList`.

---
## Key operations

- The function constructs a file path from the `ms2Folder` and `SummaryFile`.
- It loads a summary file containing MS2 spectra using `pandas`.
- It iterates through the rows of the summary, and constructs a file path for each spectrum based on the index, using the `SFindicator` to extract the spectrum id.
- It loads each MS2 spectrum from a file, and saves it to the `SpectraList`.

---
## Code

```python
import numpy as np
import pandas as pd
import os
def Retrieve_csv_ms2Spectra(SummaryFile,ms2Folder,SFindicator='-ms2Summary.xlsx'):
    SummaryFileName=ms2Folder+'/'+SummaryFile
    SummMS2=np.array(pd.read_excel(SummaryFileName,index_col=0))
    ms2FolderName=SummaryFile.replace(SFindicator,'')
    ms2FolderLoc=ms2Folder+'/'+ms2FolderName    
    N_spec=len(SummMS2[:,0])
    SpectraList=[]
    for spectrum_id in np.arange(N_spec,dtype='int'):
        FileName=ms2FolderLoc+'/'+str(spectrum_id)+'.csv'
        Exist=os.path.exists(FileName)
        if Exist:
            spectrum=np.array(pd.read_csv(FileName,index_col=0))
            SpectraList.append(spectrum)
        else:
            SpectraList.append([])
    return [SpectraList,SummMS2]

```
---

## Parameters

---

## Input

- [[ms2Folder]]
- [[SummaryFile]]
- [[SFindicator]]

---

## Output

- [[SummMS2]]
- [[SpectraList]]

---

## Functions


---

## Called by

