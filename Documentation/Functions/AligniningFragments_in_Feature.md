## Description

`AligniningFragments_in_Feature` aligns MS/MS fragments, using the `Frag_Modules` to handle clustered fragments, generating a matrix of aligned fragment data by mapping fragment intensities to different features, and it sorts the rows of the matrix based on the m/z values.

---
## Key operations

- It initializes a matrix of aligned fragments, it populates the first column with fragment m/z, and it maps fragment intensities to columns based on feature IDs, and finally sorts the matrix based on fragment m/z.

---
## Code

```python
import numpy as np
def AligniningFragments_in_Feature(Frag_Modules,All_ms2,N_features):
    N_Fragments=len(Frag_Modules)
    AlignedFragmentsMat=np.zeros((N_Fragments,N_features+1))
    for fragment_id in np.arange(N_Fragments,dtype='int'):
        Fragment_module=Frag_Modules[fragment_id]
        FragmentTable=All_ms2[Fragment_module,:]
        MaxInt=np.max(FragmentTable[:,2])
        MaxInt_Loc=np.where(FragmentTable[:,2]==MaxInt)[0]
        AlignedFragmentsMat[fragment_id,0]=FragmentTable[MaxInt_Loc,0]
        Fragments_ids=np.array(FragmentTable[:,10],dtype='int')
        AlignedFragmentsMat_loc=Fragments_ids+1
        AlignedFragmentsMat[fragment_id,AlignedFragmentsMat_loc]=FragmentTable[:,9]
    AlignedFragmentsMat=AlignedFragmentsMat[AlignedFragmentsMat[:,0].argsort()]    
    return AlignedFragmentsMat

```
---

## Parameters

---

## Input

- [[All_ms2]]
- [[N_features]]
- [[Frag_Modules]]

---

## Output

- [[AlignedFragmentsMat]]

---

## Functions


---

## Called by

- [[ms2_FeaturesDifferences]]
