## Description

The `Parameters_to_string` function transforms a list of parameters into a comma separated string, to save to a log file.

---
## Key operations

- The function iterates through the `Parameters` list, converts each element to a string, and concatenates them into a single string separated by commas. It also adds a timestamp at the beginning of the string.

---
## Code

```python
from datetime import datetime
def Parameters_to_string(Parameters):
    now =str(datetime.now())[:16]
    now=now.replace(' ','_') 
    string=','
    for par in Parameters:
        string=string+str(par)+','
    string=now+string[:-1]+'\n'
    return string

```
---

## Parameters

---

## Input

- [[Parameters]]

---

## Output

- [[string]]

---

## Functions


---

## Called by

- [[WriteLog]]
