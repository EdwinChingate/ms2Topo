![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status: Research%20Prototype](https://img.shields.io/badge/status-research%20prototype-orange)

![ms2Topo](https://github.com/EdwinChingate/ms2Gauss/blob/main/ms2Topo.png)

# ms2Topo

**Topology-driven, MS2-first feature extraction for DDA LC-HRMS**

ms2Topo is a research framework for feature extraction and cross-sample alignment in Data-Dependent Acquisition (DDA) LC-HRMS. Instead of defining features primarily from MS1 precursor traces and using MS2 only for annotation, ms2Topo treats **repeated MS2 spectra as structural evidence** and uses precursor m/z and retention time only as coarse constraints that define local search spaces.

> **Fragmentation evidence defines feature identity.**

In ms2Topo, repeated DDA spectra are not merely redundancy to be discarded. They are treated as imperfect structural replication of a latent fragmentation process. A feature is declared only when pooled spectra form a reproducible, coherent, and statistically summarizable fragmentation module.

## Why ms2Topo exists

Conventional untargeted LC-HRMS preprocessing is usually MS1-first: features are defined from precursor m/z and retention time, and MS2 is attached later. That strategy is powerful, but it is also vulnerable to chromatographic drift, adduct redundancy, in-source fragments, precursor co-isolation, and chimeric MS2 spectra.

ms2Topo was built to push **fragmentation coherence upstream** into feature construction itself. It is designed for settings where repeated DDA fragmentation events carry real structural information and where MS1-first correspondence alone is not reliable enough.

## What ms2Topo does

At a high level, the current workflow:

1. starts from a project-wide table of precursor/MS2 observations,
2. slices the data into local precursor neighborhoods,
3. builds **precursor ambiguity sets** rather than immediate final features,
4. retrieves and pools the underlying MS2 spectra,
5. aligns fragment peaks into a common fragment-by-spectrum representation,
6. compresses the aligned matrix to recurrent and intensity-explaining fragments,
7. computes pairwise spectral similarity,
8. partitions the similarity structure into coherent spectral modules,
9. summarizes accepted modules into robust consensus spectra, and
10. exports **fragmentation-defined feature objects** with support and dispersion metadata.

The result is not just a precursor peak with an attached spectrum. It is a **consensus-bearing analytical feature** supported by repeated fragmentation evidence.

## Current methodological interpretation

The current conceptual center of ms2Topo is an **MS2-first, spectral-clustering-centered workflow**. Precursor m/z and retention time do matter, but mainly as permissive constraints for building local ambiguity sets. They are not treated as the final identity-bearing definition of the feature.

Within each ambiguity set, ms2Topo moves through a sequence of data transformations:

- precursor observations become local search spaces,
- local search spaces become pooled fragment evidence,
- pooled fragment evidence becomes an aligned fragment matrix,
- the aligned matrix becomes a similarity graph,
- the similarity graph becomes one or more spectral partitions,
- and those partitions become consensus-bearing feature objects.

In ms2Topo **a stable analytical feature should be supported by reproducible fragmentation structure**.

## Core workflow logic

### 1. Precursor ambiguity sets

`ms2_SamplesAligment` orchestrates the workflow slice by slice in precursor space. `EdgesMat` defines local m/z windows, `AdjacencyListFeatures` builds precursor-space adjacency relationships from m/z and retention-time overlap, and `ms2_feat_modules` extracts connected components.

These connected components are **not yet final features**. They are precursor ambiguity sets: local groups of observations that may correspond to one analyte, several isomers, or a chimeric mixture.

### 2. Fragment alignment

For each ambiguity set, `Retrieve_and_Join_ms2_for_feature` loads the underlying MS2 spectra and pools their fragment peaks. `AdjacencyList_ms2Fragments` groups fragment observations under m/z tolerance, and `AligniningFragments_in_Feature` maps them into a shared fragment-by-spectrum representation.

This step is essential. Raw spectra are irregular peak lists; without a shared coordinate system, cosine similarity and downstream matrix operations would not be meaningful.

### 3. Recurrence-aware compression

`minimalAlignedFragmentsMat` and `minimalSpectrum` reduce the aligned representation to fragments that are both recurrent and intensity-explaining. The goal is not to preserve every observed ion, but to emphasize structural fragments that recur strongly enough to support a stable feature definition.

### 4. Similarity-based partitioning

`CosineMatrix` computes pairwise similarity in aligned fragment space. The current conceptual prototype is centered on **spectral clustering** with **silhouette-like cohesion/separation logic** rather than on a fixed cosine threshold or purely greedy local community detection.

This matters because the role of clustering in ms2Topo is not just organizational. It decides whether a coarse precursor neighborhood contains one fragmentation-defined feature or several more coherent subfeatures.

### 5. Consensus feature construction

Accepted spectral modules are summarized by `ConsensusSpectra` and `ConsensusFragment` using robust, non-parametric statistics such as medians, percentiles, and dispersion summaries. The output is a consensus representation of repeated DDA evidence, not a simple average and not a single chosen scan.

## Inputs

The current workflow is designed around three main input layers:

1. **A project-wide precursor/MS2 summary table** containing precursor-level observations.
2. **Local precursor slicing information** such as `EdgesMat` to bound comparisons in m/z space.
3. **Underlying MS2 spectra on disk**, retrieved for each provisional feature module.


## Outputs

ms2Topo currently export:

- consensus spectra,
- feature-level provenance,
- descriptor-rich rows in an aligned feature table,
- support and cohesion/separation summaries,
- cross-sample occurrence metadata.

## What ms2Topo is and is not

ms2Topo is:

- an **MS2-first framework** for DDA LC-HRMS feature construction,
- a **mid-pipeline structural inference layer**,
- a bridge between feature extraction, spectrum clustering, graph partitioning, and consensus-spectrum generation,
- a way to construct **fragmentation-defined analytical features with explicit support and uncertainty**.

ms2Topo is not:

- a claim to recover final chemical truth from MS2 alone,
- a replacement for orthogonal identification, standards, library matching, or downstream annotation tools,
- a polished general-purpose Python package with a stable public API,

Closely related stereoisomers, repeated co-isolation patterns, adduct heterogeneity, or unstable fragmentation regimes can still remain difficult. ms2Topo is strongest when interpreted as a method for constructing **stable analytical features from repeated fragmentation evidence**, not as a universal solver of chemical identity.

## Scientific positioning

ms2Topo sits between several established method families:

- MS1-first feature extraction and alignment workflows,
- spectral networking and feature-based molecular networking,
- spectrum clustering and consensus-spectrum generation,
- similarity-based MS/MS representation methods.

It is the decision to make **fragmentation coherence part of feature declaration itself**.

## Current repository status

Immediate priorities for the project include:

- stabilizing data-object schemas,
- clarifying the canonical clustering backend,
- improving provenance and uncertainty reporting,
- packaging the workflow more rigorously,
- and benchmarking partition stability and downstream usefulness.

## Recommended use cases

ms2Topo is especially relevant for:

- DDA metabolomics and non-target screening,
- studies where repeated MS2 evidence is abundant,
- cases with precursor ambiguity or unstable MS1 correspondence,
- chimericity-aware feature construction,
- isomer-rich or structurally complex datasets,
- workflows that benefit from consensus-level fragmentation objects before downstream annotation.

## Citation

If you use ms2Topo in research, please cite the repository and the associated manuscript or preprint when available.

## Maintainer

**Edwin Chingate**

ms2Topo emerged from PhD research on microbial transformation of pharmaceutical compounds using LC-HRMS. The project grows from the observation that repeated DDA spectra should be treated as structural evidence rather than as disposable redundancy, and that feature construction can be improved by working directly with fragmentation topology.

- Email: edwinchingate@gmail.com
- LinkedIn: https://www.linkedin.com/in/edwinchingate/

## Opportunities

If ms2Topo is relevant to your lab, platform, or product roadmap, I would be glad to connect about collaboration, scientific software work, or computational MS/MS development.

