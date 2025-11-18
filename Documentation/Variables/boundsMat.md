## Description

boundsMat` is a NumPy array that stores boundaries for Gaussian fitting parameters. It is generated in `GaussBoundaries` and used in multiple functions like `NPeaksRestrict`, `ParametersFitGaussPeaks`, `ParametersFitGaussParallelPeaks`, `RawGaussSeed`, `RefineParameters`, `RefinePop_OnePeak`, `RefineChromPeak`, `RestrictStdPeaks`, `RawGaussParameters`, `RawGaussCouple` and `RawParametersCut`, and in mutation functions, to define valid ranges for parameter values or to refine parameter values. It is also used in `UniquePeaks` and `RefineParametersPopulation`.

---

## Functions using

- [[MutantOffspring]]
- [[NPeaksRestrict]]
- [[RefineParametersPopulation]]
- [[MutationTimes]]
- [[Mate_MutantGenerations]]
- [[Mate_square_WildPop]]
- [[RawGaussCouple]]
- [[RestrictStdPeaks]]
- [[RawParametersCut]]
- [[RawGaussParameters]]
- [[ParametersFitGaussPeaks]]
- [[UniquePeaks]]
- [[RefinePop_OnePeak]]
- [[RefineChromPeak]]
- [[GaussBoundaries]]
- [[Mate_WildGenerations]]
- [[Mutate]]
- [[Mate_FineGenerations]]
- [[ParametersFitGaussParallelPeaks]]
- [[RawGaussSeed]]
- [[RefineParameters]]
