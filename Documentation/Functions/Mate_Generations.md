## Description

The `Mate_Generations` function evolves a population of parameter sets by mating using `Mate_square_GaussParPop`, evaluating using `EvaluatePopulation`, and selecting the best individuals using `FitnessSelector`, repeating the process `Generations` times and selecting the best `NSelect` individuals.

---
## Key operations

- It performs a series of mating events using the function `Mate_square_GaussParPop`, which combines the parameters of individuals in the population to create new parameter sets. It then evaluates the fitness of the new individuals by using the function `EvaluatePopulation`. Finally, the function selects the best individuals using `FitnessSelector`. This process repeats `Generations` number of times.

---
## Code

```python
from Mate_square_GaussParPop import *
from EvaluatePopulation import *
from FitnessSelector import *
def Mate_Generations(Population,smooth_peaks,Generations=5,NSelect=10):    
    for generation in np.arange(Generations):
        Population=Mate_square_GaussParPop(SeedPopulation=Population) 
        Population=Mate_square_GaussParPop(SeedPopulation=Population)         
        r2Vec=EvaluatePopulation(Population=Population,smooth_peaks=smooth_peaks)
        Population,r2ListFit=FitnessSelector(r2Vec=r2Vec,Population=Population,NSelect=NSelect) 
    return [Population,r2ListFit]

```
---

## Parameters

---

## Input

- [[Generations]]
- [[Population]]
- [[NSelect]]
- [[smooth_peaks]]

---

## Output

- [[r2ListFit]]
- [[Population]]

---

## Functions

- [[FitnessSelector]]
- [[Mate_square_GaussParPop]]
- [[EvaluatePopulation]]

---

## Called by

- [[RefinePop_OnePeak]]
- [[GeneticChromatogram]]
