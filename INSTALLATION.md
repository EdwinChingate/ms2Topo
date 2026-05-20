# Installation

This page explains how to install and run **ms2Topo** from a local checkout of the GitHub repository.

ms2Topo is currently a research-prototype workflow rather than a packaged Python library. The recommended installation is therefore:

1. clone or download the repository,
2. install the scientific Python dependencies,
3. run the example notebook from the repository root.

Creating a clean Python environment is recommended, especially if you want a reproducible setup or if you already use Python for other projects. However, it is not strictly required. If you already have a working Python installation, you can install the required packages there and run the notebook directly.

---

## 1. Requirements

Recommended operating system:

- Linux, macOS, or Windows with a 64-bit Python installation.

Recommended Python version:

- Python 3.11 is a safe choice for the current workflow.
- pyOpenMS currently supports Python 3.9–3.13, so avoid older Python versions.

Core Python dependencies used by the current repository:

```bash
numpy
pandas
scipy
scikit-learn
pyopenms
openpyxl
jupyter
ipython
tabulate
```

What these are used for:

- `numpy`: matrix operations, fragment alignment, cosine matrices, clustering summaries.
- `pandas`: reading and writing feature tables, MS2 summary tables, and consensus spectra.
- `scikit-learn`: spectral clustering.
- `scipy`: numerical backend used by parts of the clustering stack.
- `pyopenms`: reading mzML files and extracting MS/MS spectra.
- `openpyxl`: Excel input/output through pandas.
- `jupyter`, `ipython`, `tabulate`: running and displaying the example notebook.

---

## 2. Clone the repository

Using Git:

```bash
git clone https://github.com/EdwinChingate/ms2Topo.git
cd ms2Topo
```

Alternatively, download the repository as a ZIP file from GitHub, unzip it, and open a terminal inside the extracted `ms2Topo` folder.

---

## 3. Install the Python dependencies

You do not need to be a software developer to try ms2Topo. The simplest route is to use the Python installation you already have and install the required packages there.

From the repository root, you can try:

```bash
python -m pip install numpy pandas scipy scikit-learn pyopenms openpyxl jupyter ipython tabulate
```

If that works, you can continue directly to the installation check below.

That said, creating a separate environment is a good practice because it keeps ms2Topo's dependencies isolated from other Python projects. This is especially useful if you already have many scientific Python packages installed, or if you want to reproduce the same setup later.

### Option A: Conda environment

```bash
conda create -n ms2topo python=3.11 -y
conda activate ms2topo
python -m pip install --upgrade pip
```

Then install the required packages:

```bash
python -m pip install numpy pandas scipy scikit-learn pyopenms openpyxl jupyter ipython tabulate
```

### Option B: venv environment

On Linux or macOS:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install numpy pandas scipy scikit-learn pyopenms openpyxl jupyter ipython tabulate
```

On Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy pandas scipy scikit-learn pyopenms openpyxl jupyter ipython tabulate
```

---

## 4. Check the installation

From the repository root, run:

```bash
python - <<'PY'
import numpy
import pandas
import sklearn
from pyopenms import MSExperiment, MzMLFile

print("Core dependencies imported successfully.")
PY
```

Then check that Python can see the local ms2Topo functions:

```bash
python - <<'PY'
import os
import sys

repo_root = os.getcwd()
sys.path.append(os.path.join(repo_root, "Functions"))

from ms2_SamplesAligment import *
from BatchExtract_All_MS2_Spectra import *
from JoiningSummMS2 import *
from WorkLoadPlanning import *

print("ms2Topo local functions imported successfully.")
PY
```

If this second check fails, make sure you are running the command from the root of the cloned repository, not from inside `Functions/` or another folder.

---

## 5. Run the example notebook

Start Jupyter from the repository root:

```bash
jupyter notebook ms2Topo.ipynb
```

or:

```bash
jupyter lab ms2Topo.ipynb
```

The example notebook follows the current workflow:

1. extract MS2 spectra from mzML files,
2. join sample-level MS2 summary tables,
3. define m/z workload slices,
4. set workflow parameters,
5. run `ms2_SamplesAligment`,
6. inspect the aligned feature table and consensus spectra.

The notebook adds the local `Functions/` folder to the Python path with:

```python
import sys
import os

home = os.getcwd()
sys.path.append(home + "/Functions")
```

For this reason, the notebook should be run from the repository root.

---

## 6. Expected input layout

The example workflow assumes a project layout similar to:

```text
ms2Topo/
├── Functions/
├── Playground/
│   ├── Data/
│   │   ├── sample_A.mzML
│   │   ├── sample_B.mzML
│   │   └── ...
│   └── ms2_spectra-YYYYMMDD/
├── ms2Topo.ipynb
└── README.md
```

The raw mzML files should be placed in the data folder used by the notebook, for example:

```python
DataFolder = home + "/Playground/Data"
```

The extracted MS2 spectra are written to a folder such as:

```python
saveFolder = home + "/Playground/ms2_spectra-20260520"
```

The main alignment step later reads from that folder through:

```python
params["io"]["ms2Folder"]
```

---

## 7. Minimal usage pattern

After extracting and joining MS2 spectra, the central workflow is:

```python
from ms2_SamplesAligment import *
from make_ms2topo_context import *

context = make_ms2topo_context(ProjectName = ProjectName,
                               All_SummMS2Table = All_SummMS2Table,
                               EdgesMat = EdgesMat,
                               SamplesNames = SamplesNames,
                               feature_id = 0)

AlignedSamplesDF = ms2_SamplesAligment(context = context,
                                       params = params)
                                       
```

The most important objects are:

- `All_SummMS2Table`: project-wide precursor/MS2 summary table.
- `EdgesMat`: m/z slice boundaries used to divide the workload.
- `SamplesNames`: sample names used to retrieve spectra and label output columns.
- `params`: dictionary controlling input/output paths, feature grouping, fragment alignment, spectral clustering, and consensus-feature closing.
- `AlignedSamplesDF`: final aligned feature table returned by the workflow.

---

## 8. Expected outputs

Running the workflow writes two main types of output:

1. Feature tables such as:

```text
ms2Topo_Features_table-0.csv
```

2. A dated consensus-output folder such as:

```text
Alignedms2Features2026-05-20/
```

The dated folder contains:

- consensus MS2 spectra,
- feature-to-spectrum provenance tables,
- information needed to trace each final ms2Topo feature back to its contributing MS2 observations.

---

## 9. Troubleshooting

### `ModuleNotFoundError` for a local ms2Topo function

Make sure you are running Python or Jupyter from the repository root and that `Functions/` has been added to `sys.path`:

```python
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "Functions"))
```

### `ModuleNotFoundError: No module named 'pyopenms'`

Install pyOpenMS in the active environment:

```bash
python -m pip install pyopenms
```

Also check that your Python version is supported:

```bash
python --version
```

### `ImportError` or Excel read/write errors

Install `openpyxl`:

```bash
python -m pip install openpyxl
```

This is needed because the current workflow reads and writes Excel files through pandas.

### Spectral clustering warnings

You may see warnings from scikit-learn when a similarity graph is small, sparse, or not fully connected. These warnings usually indicate a data/clustering condition rather than a missing installation dependency. If the workflow fails at the clustering step, first check:

- number of spectra in the current precursor ambiguity set,
- `params["clustering"]["Nspectra_sampling"]`,
- `params["clustering"]["max_Nspectra_cluster"]`,
- `params["clustering"]["min_nodes"]`,
- whether the cosine matrix contains invalid or degenerate values.

### Running from the wrong directory

Many paths in the example notebook are relative to the repository root. If files are not found, check:

```python
import os
print(os.getcwd())
```

Then restart Jupyter from the root `ms2Topo/` folder.

---

## 10. Development notes

At this stage, ms2Topo is installed by working directly from the source tree. A future packaging step could add:

- `pyproject.toml`,
- `requirements.txt` or `environment.yml`,
- a proper package namespace,
- command-line entry points,
- automated installation tests.

Until then, the safest reproducible setup is to clone the repository, install the dependencies in a clean environment, and run the notebook from the repository root.
