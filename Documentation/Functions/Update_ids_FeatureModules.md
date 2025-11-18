## Description

`Update_ids_FeatureModules` iterates through a list of feature modules, updating the feature identifiers in place, returning the updated list of modules.

---
## Key operations

- The function iterates through each module in `Feature_Modules` and updates the identifiers, returning the updated `Modules` variable. The specific updating method is not described in the source code.

---
## Code

```python
import numpy as np
def Update_ids_FeatureModules(Feature_module,Feature_Modules):
    npFeature_module=np.array(Feature_module)
    Modules=[]
    for module in Feature_Modules:
        feature_module=list(npFeature_module[module])
        Modules.append(feature_module)
    return Modules

```
---

## Parameters

---

## Input

- [[Feature_module]]
- [[Feature_Modules]]

---

## Output

- [[Modules]]

---

## Functions


---

## Called by

- [[ms2_FeaturesDifferences]]
