## Description

`ShowPop` displays a list of parameter matrices. It iterates through the `Population` list and uses the `ShowDF` function to display each matrix as a formatted HTML table.

---
## Key operations

- It loops through the `Population` and calls `ShowDF` for each individual.

---
## Code

```python
from ShowDF import *
def ShowPop(Population):
    for individual in Population:
        ShowDF(individual)

```
---

## Parameters

---

## Input

- [[Population]]

---

## Output


---

## Functions

- [[ShowDF]]

---

## Called by

