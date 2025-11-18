## Description

The `Mate_MutantGenerations` function evolves a population of parameter sets by mating using `Mate_square_GaussParPop`, mutating using `MutationTimes`, evaluating using `EvaluatePopulation`, and selecting the best individuals using `FitnessSelector`, repeating the process `Generations` times and selecting the best `NSelect` individuals.

---
## Key operations

- It performs a series of mating events using the function `Mate_square_GaussParPop`, which combines the parameters of individuals in the population to create new parameter sets. Then, it introduces mutations into the population using the function `MutationTimes`, which uses the `mut_stdVec` to control the mutation magnitudes, and also uses the `boundsMat` to ensure that the parameters remain within the boundaries defined for the Gaussian fitting. It then evaluates the fitness of the new individuals by using the function `EvaluatePopulation`. Finally, the function selects the best individuals using `FitnessSelector`. This process repeats `Generations` number of times.

---
## Code

```python
from Mate_square_GaussParPop import *
from EvaluatePopulation import *
from FitnessSelector import *
from MutationTimes import *
def Mate_MutantGenerations(Population,smooth_peaks,boundsMat,mut_stdVec=[0.6,0.7,0.8],Generations=5,NSelect=5,Mutants=5):    
    for generation in np.arange(Generations):
        Population=Mate_square_GaussParPop(SeedPopulation=Population)
        mut_stdVec=mut_stdVec/(generation*10+1)
        Population=MutationTimes(Population=Population,mut_stdVec=mut_stdVec,boundsMat=boundsMat,Mutants=Mutants)
        r2Vec=EvaluatePopulation(Population=Population,smooth_peaks=smooth_peaks)
        Population,r2ListFit=FitnessSelector(r2Vec=r2Vec,Population=Population,NSelect=NSelect) 
    return [Population,r2ListFit]

```
---

## Parameters

---

## Input

- [[Generations]]
- [[mut_stdVec]]
- [[Population]]
- [[0.7]]
- [[0.8]]
- [[Mutants]]
- [[boundsMat]]
- [[NSelect]]
- [[smooth_peaks]]

---

## Output

- [[r2ListFit]]
- [[Population]]

---

## Functions

- [[FitnessSelector]]
- [[MutationTimes]]
- [[Mate_square_GaussParPop]]
- [[EvaluatePopulation]]

---

## Called by

- [[GeneticChromatogram]]
