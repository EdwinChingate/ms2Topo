## Description

The `Mate_WildGenerations` function evolves a population of parameter sets by mating using `Mate_square_WildPop`, evaluating using `EvaluatePopulation`, and selecting the best individuals using `FitnessSelector`, repeating the process `Generations` times and selecting the best `NSelect` individuals, using `boundsMat` to define the boundaries for the Gaussian parameters, and `NOffspring` to control the number of offspring.

---
## Key operations

- It performs a series of mating events using the function `Mate_square_WildPop`, which combines the parameters of individuals in the population to create new parameter sets, while also using the `boundsMat` and `NOffspring` parameters to create the new offspring. It then evaluates the fitness of the new individuals by using the function `EvaluatePopulation`. Finally, the function selects the best individuals using `FitnessSelector`. This process repeats `Generations` number of times.

---
## Code

```python
from Mate_square_WildPop import *
from EvaluatePopulation import *
from FitnessSelector import *
def Mate_WildGenerations(Population,smooth_peaks,boundsMat,Generations=5,NSelect=10,NOffspring=10):    
    for generation in np.arange(Generations):
        Population=Mate_square_WildPop(SeedPopulation=Population,boundsMat=boundsMat,NOffspring=NOffspring) 
        r2Vec=EvaluatePopulation(Population=Population,smooth_peaks=smooth_peaks)        
        Population,r2ListFit=FitnessSelector(r2Vec=r2Vec,Population=Population,NSelect=NSelect) 
    return [Population,r2ListFit]

```
---

## Parameters

---

## Input

- [[Generations]]
- [[NOffspring]]
- [[Population]]
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
- [[Mate_square_WildPop]]
- [[EvaluatePopulation]]

---

## Called by

