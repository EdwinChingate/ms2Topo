## Description

The `GoodNeigbour` function compares two MS2 spectra using `Similarity_2Spectra`, returning an updated `AdjacencyMatrix` that indicates whether the spectra are neighbors based on the `min_Int_Frac`, `Tanimoto_tol`, and `cos_tol` similarity thresholds.

---
## Key operations

- It calculates the Tanimoto and cosine similarity scores between two input spectra, using `Similarity_2Spectra`, and it updates the `AdjacencyMatrix` if the spectra are deemed neighbors based on the `Tanimoto_tol`, and `cos_tol` values.

---
## Code

```python
from Similarity_2Spectra import *
def GoodNeigbour(ms2_candidate_id1,ms2_candidate_id2,AdjacencyMatrix,Spectrum_1,Spectrum_2,min_Int_Frac,Tanimoto_tol,cos_tol):
    Cosine,TanimotoSim=Similarity_2Spectra(Spectrum_1=Spectrum_1,Spectrum_2=Spectrum_2,min_Int_Frac=min_Int_Frac)
    if Cosine>cos_tol and TanimotoSim>Tanimoto_tol:
        AdjacencyMatrix[ms2_candidate_id1,ms2_candidate_id2]=1
        AdjacencyMatrix[ms2_candidate_id2,ms2_candidate_id1]=1
    return AdjacencyMatrix

```
---

## Parameters

---

## Input

- [[Spectrum_2]]
- [[ms2_candidate_id2]]
- [[Tanimoto_tol]]
- [[AdjacencyMatrix]]
- [[Spectrum_1]]
- [[cos_tol]]
- [[min_Int_Frac]]
- [[ms2_candidate_id1]]

---

## Output

- [[AdjacencyMatrix]]

---

## Functions

- [[Similarity_2Spectra]]

---

## Called by

- [[CheckNeigbours]]
