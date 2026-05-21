![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status: Research%20Prototype](https://img.shields.io/badge/status-research%20prototype-orange)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20320152.svg)](https://doi.org/10.5281/zenodo.20320152)

![ms2Topo](ms2Topo.png)

# ms2Topo

**MS2-first feature construction for DDA LC-HRMS**

ms2Topo is a research prototype for building reproducible analytical features from Data-Dependent Acquisition (DDA) LC-HRMS/MS data.

Most untargeted workflows begin with MS1 features: boxes in *m/z* and retention time. MS2 spectra are then attached later as annotation evidence. That workflow is useful, but it can hide a difficult problem: a single MS1 neighborhood may contain adducts, in-source fragments, co-eluting isomers, or chimeric MS2 spectra.

ms2Topo uses precursor *m/z* and retention time as coarse boundaries, then asks whether the repeated MS2 evidence inside those boundaries supports one coherent fragmentation pattern or several. It reconstructs stable, fragmentation-consistent analytical features. The output is a cleaner, support-aware analytical object that can be used more safely before downstream annotation, library matching, molecular networking, or manual interpretation.

---

## Why this matters

DDA MS2 spectra are often treated as redundant scans that can be averaged, discarded, or represented by a single “best” spectrum. In practice, repeated MS2 scans are more complicated. They are partial observations of a latent fragmentation process, affected by signal intensity, chromatographic context, co-isolation, missing fragments, and instrumental variability.

That means repeated spectra can contain useful structural evidence, but only if they are compared in a shared fragment space and summarized carefully.

ms2Topo was built around this idea:

1. **MS1 coordinates define ambiguity sets, not final identities.**
2. **Fragment alignment makes MS2 spectra comparable.**
3. **Spectral similarity organizes repeated fragmentation evidence.**
4. **Spectral clustering separates coherent MS2 modules.**
5. **Robust consensus construction turns each module into a stable analytical feature.**

---

## What ms2Topo does

At a high level, ms2Topo:

1. starts from a project-wide table of precursor/MS2 observations,
2. divides the data into local *m/z* workload slices,
3. groups nearby precursor observations into **precursor ambiguity sets**,
4. retrieves the underlying MS2 spectra for each ambiguity set,
5. aligns fragment peaks into a common fragment-by-spectrum matrix,
6. keeps recurrent and intensity-explaining fragments,
7. computes pairwise cosine similarity between spectra,
8. partitions the similarity graph into coherent spectral modules,
9. summarizes each accepted module into a robust consensus spectrum, and
10. exports feature tables, consensus spectra, and provenance files.

The final feature is defined by reproducible fragmentation structure, not by MS1 coordinates alone.

---

## Quick start

See [`INSTALLATION`](INSTALLATION.md) for setup instructions.

Clone the repository, install the dependencies, then open:

```bash
jupyter notebook ms2Topo.ipynb
```

The full example workflow is available in [`ms2Topo`](ms2Topo.ipynb)

---

## Documentation

For a workflow-oriented function reference, see the documentation wiki:

<https://github.com/EdwinChingate/ms2Topo/wiki>

The wiki follows the main data transformation from `.mzML` files and precursor/MS2 summaries to fragment alignment, spectral clustering, consensus spectra, and final ms2Topo feature objects.

---

## Inputs

ms2Topo starts from `.mzML` files acquired by DDA LC-HRMS/MS. The example notebook extracts MS2 spectra from these files and builds the intermediate tables used by the alignment workflow.

---

## Outputs

ms2Topo writes two main kinds of output.

### 1. Aligned feature table

The main table contains one row per final ms2Topo feature object. It summarizes:

- precursor *m/z* and retention-time statistics,
- number of samples,
- number of supporting MS2 spectra,
- spectral-clustering quality summaries,
- intramodule cosine-similarity summaries,
- sample-level occurrence metadata.

At the current prototype stage, the sample columns should be read primarily as occurrence/presence metadata.

### 2. Consensus spectra and provenance files

The workflow also writes a dated folder such as:

```text
Alignedms2Features2026-05-20/
```

This folder contains:

- consensus MS2 spectra,
- feature-to-spectrum provenance tables,
- information needed to trace each final feature back to the MS2 observations that produced it.

---

## Working principle

### 1. Precursor ambiguity sets

`ms2_SamplesAligment` orchestrates the workflow across *m/z* slices. Within each slice, `AdjacencyListFeatures` groups precursor observations by *m/z* and retention-time overlap. `ms2_feat_modules` then extracts connected components.

These connected components are not final features. They are **precursor ambiguity sets**: local neighborhoods that may contain one analyte, several related analytes, or a chimeric mixture.

### 2. Fragment alignment

For each ambiguity set, `Retrieve_and_Join_ms2_for_feature` retrieves the underlying MS2 spectra and pools their fragment peaks. `AdjacencyList_ms2Fragments` groups fragment observations by *m/z* proximity, and `AligniningFragments_in_Feature` maps them into an aligned fragment-by-spectrum matrix.

This step is essential. Raw MS2 spectra are irregular peak lists. They must be aligned before cosine similarity, clustering, or consensus construction can be interpreted.

### 3. Recurrence-aware compression

`minimalAlignedFragmentsMat` and `minimalSpectrum` reduce the aligned matrix to fragments that explain most of the spectral intensity and recur strongly enough to support a stable feature definition. The purpose is to keep the fragments most likely to represent reproducible structural evidence.

### 4. Similarity graph and spectral clustering

`CosineMatrix` computes pairwise spectral similarity in aligned fragment space. The current prototype then evaluates candidate partitions using spectral clustering and a similarity-based cohesion/separation logic.

This is the point where ms2Topo asks:

> Does this precursor ambiguity set contain one coherent fragmentation pattern, or should it be split into multiple fragmentation-consistent modules?

### 5. Consensus feature construction

Accepted spectral modules are closed into feature objects. `ConsensusSpectra` and `ConsensusFragment` summarize aligned fragments using robust statistics such as medians, percentiles, support counts, and dispersion summaries.

This produces a consensus-bearing analytical feature. It is more stable than a single scan and safer than a naive average, but it is still an analytical feature, not a confirmed molecular identity.

---

## Function map

| Stage | Main functions | Role |
|---|---|---|
| MS2 extraction and preparation | `BatchExtract_All_MS2_Spectra`, `JoiningSummMS2`, `WorkLoadPlanning` | Build the project-level MS2 summary table and workload slices. |
| Workflow orchestration | `ms2_SamplesAligment`, `ms2_SpectralSimilarityClustering`, `ms2_FeaturesDifferences` | Run the slice-wise and module-wise ms2Topo workflow. |
| Precursor ambiguity sets | `AdjacencyListFeatures`, `ms2_feat_modules`, `AdjacencyClustering` | Group nearby precursor observations before MS2 refinement. |
| Fragment alignment | `Retrieve_and_Join_ms2_for_feature`, `AlignFragmentsEngine`, `AdjacencyList_ms2Fragments`, `AligniningFragments_in_Feature` | Retrieve spectra and align fragment peaks into a shared matrix. |
| Fragment filtering | `minimalAlignedFragmentsMat`, `minimalSpectrum` | Keep recurrent and intensity-explaining fragments. |
| Similarity and partitioning | `CosineMatrix`, `sklearn_spectral_modules_from_cosine_matrix`, `estimate_k_by_resampled_spectral_clustering`, `evaluate_n_partitions` | Build the similarity graph and estimate spectral modules. |
| Quality summaries | `silhouette_vector_calculator`, `all_modules_silhouette_vector_summarizer`, `IntramoduleSimilarityCalc` | Summarize cohesion, separation, and intramodule similarity. |
| Consensus closing | `ConsensusSpectra`, `ConsensusFragment`, `FeatureModuleStats`, `Write_ms2ids_and_Consensus_ms2Spectra`, `ClosingModule`, `Update_ids_FeatureModules` | Write consensus spectra, provenance files, and aligned feature rows. |

---

## What ms2Topo is

ms2Topo is:

- an **MS2-first feature-construction framework** for DDA LC-HRMS/MS,
- a **mid-pipeline structural inference layer**,
- a way to turn precursor ambiguity sets into stable, fragmentation-consistent analytical features,
- a graph- and consensus-based bridge between raw MS2 evidence and downstream annotation.

---

## What ms2Topo is not

ms2Topo is not:

- a final chemical identification tool,
- a substitute for reference standards or orthogonal validation,
- a complete replacement for downstream annotation tools,
- a polished general-purpose Python package with a stable public API.

Spectral similarity can organize evidence, but it does not prove chemical identity. Consensus construction improves stability, but it does not solve isomerism. ms2Topo makes the analytical object cleaner and more explicit; it does not remove every physical ambiguity in LC-HRMS/MS.

---

## Recommended use cases

ms2Topo is especially relevant for:

- DDA metabolomics,
- non-target screening,
- datasets with repeated MS2 evidence,
- isomer-rich or structurally complex samples,
- workflows that need consensus-level MS2 objects before annotation.

---

## Current status

ms2Topo is under active development. The current repository should be read as a research prototype and a working method demonstration.

Near-term priorities include:

- packaging the workflow more rigorously,
- improving integration with chromatographic data.

---

## Repository structure

```text
ms2Topo/
├── Functions/              # Core workflow functions
├── Playground/             # Example data and working folders
├── INSTALLATION.md         # Installation guide
├── LICENSE.md              # MIT license
├── README.md               # Project overview
├── ms2Topo.ipynb           # Example notebook
└── ms2Topo.png             # Project image
```

---

## Citation

If you use ms2Topo in research, please cite the archived Zenodo release:

> Chingate, E. (2026). ms2Topo: MS2-first feature construction for DDA LC-HRMS/MS. Zenodo. https://doi.org/10.5281/zenodo.20320152

Please also cite the GitHub repository when referring to the active development version:

<https://github.com/EdwinChingate/ms2Topo>

---

## License

This project is released under the MIT License. See [`LICENSE`](LICENSE.md).

---

## Developer and maintainer

**Edwin Chingate**  
Colombia

ms2Topo originated from my PhD research on microbial transformation of pharmaceutical compounds using DDA LC-HRMS/MS. While analyzing years of MS/MS data, I became interested in a recurring problem: many workflows treat repeated DDA spectra as redundancy or noise, while relying heavily on MS1-first feature definitions.

I built ms2Topo to explore a different strategy. The framework treats repeated MS2 spectra as statistical replication of fragmentation evidence and declares analytical features only when the spectra form stable, coherent communities in similarity space.

I am currently completing my PhD dissertation and am open to paid roles, research collaborations, or contract work in computational mass spectrometry and scientific software. Relevant roles include:

- Computational Mass Spectrometry Scientist
- Scientific Software Engineer
- Research Software Engineer
- Computational Metabolomics / Non-target Screening Scientist

I am especially interested in teams working with real LC-HRMS/MS datasets, DDA/DIA workflows, metabolomics, non-target screening, spectral similarity, molecular networking, or scientific software infrastructure.

If ms2Topo is relevant to your lab, platform, or product roadmap, I would be happy to talk.

- Email: edwinchingate@gmail.com
- LinkedIn: <https://www.linkedin.com/in/edwinchingate/>
