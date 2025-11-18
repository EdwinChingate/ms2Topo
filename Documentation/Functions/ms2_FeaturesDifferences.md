## Description

The function identifies groups of related MS2 fragments, aligns them, calculates their spectral similarity, and clusters them into modules, enabling the identification of differences between MS2 features across samples.

---
## Key operations

- It retrieves MS2 spectra using `Retrieve_and_Join_ms2_for_feature`.
- It constructs an adjacency list of fragments using `AdjacencyList_ms2Fragments`.
- It clusters the fragments into modules using `ms2_feat_modules`.
- It aligns fragments using `AligniningFragments_in_Feature`.
- It computes a cosine similarity matrix using `CosineMatrix`.
- It generates an adjacency list from the similarity matrix using `AdjacencyList_from_matrix`.
- It performs clustering on the features using `ms2_feat_modules`.
- It updates feature IDs using `Update_ids_FeatureModules`.

---
## Code

```python
from Retrieve_and_Join_ms2_for_feature import *
from AdjacencyList_ms2Fragments import *
from ms2_feat_modules import *
from AligniningFragments_in_Feature import *
from CosineMatrix import *
from AdjacencyList_from_matrix import *
from ms2_feat_modules import *
from Update_ids_FeatureModules import *
def ms2_FeaturesDifferences(All_FeaturesTable,Feature_module,SamplesNames,sample_id_col=16,ms2_spec_id_col=15,ms2Folder='ms2_spectra',ToAdd='mzML',min_Int_Frac=2,cos_tol=0.9):
    All_ms2=Retrieve_and_Join_ms2_for_feature(All_FeaturesTable=All_FeaturesTable,Feature_module=Feature_module,SamplesNames=SamplesNames,sample_id_col=sample_id_col,ms2_spec_id_col=ms2_spec_id_col,ms2Folder=ms2Folder,ToAdd=ToAdd,min_Int_Frac=min_Int_Frac)
    if len(All_ms2)==0:
        return []
    AdjacencyListFragments,feat_ids=AdjacencyList_ms2Fragments(All_ms2=All_ms2)
    N_features=len(Feature_module)
    Frag_Modules=ms2_feat_modules(AdjacencyList=AdjacencyListFragments,ms2_ids=feat_ids)
    AlignedFragmentsMat=AligniningFragments_in_Feature(Frag_Modules=Frag_Modules,All_ms2=All_ms2,N_features=N_features)    
    CosineMat=CosineMatrix(AlignedFragmentsMat=AlignedFragmentsMat,N_features=N_features)
    AdjacencyList_Features,features_ids=AdjacencyList_from_matrix(AdjacencyMatrix=CosineMat,N_ms2_spectra=N_features,minAdjacency=cos_tol)
    Feature_Modules=ms2_feat_modules(AdjacencyList=AdjacencyList_Features,ms2_ids=features_ids)
    Feature_Modules=Update_ids_FeatureModules(Feature_module=Feature_module,Feature_Modules=Feature_Modules)
    return Feature_Modules

```
---

## Parameters

---

## Input

- [[ms2Folder]]
- [[All_FeaturesTable]]
- [[sample_id_col]]
- [[SamplesNames]]
- [[cos_tol]]
- [[min_Int_Frac]]
- [[ms2_spec_id_col]]
- [[Feature_module]]
- [[ToAdd]]

---

## Output

- [[]]
- [[Feature_Modules]]

---

## Functions

- [[ms2_feat_modules]]
- [[AdjacencyList_ms2Fragments]]
- [[Update_ids_FeatureModules]]
- [[AdjacencyList_from_matrix]]
- [[Retrieve_and_Join_ms2_for_feature]]
- [[AligniningFragments_in_Feature]]
- [[CosineMatrix]]

---

## Called by

- [[ms2_SpectralSimilarityClustering]]
