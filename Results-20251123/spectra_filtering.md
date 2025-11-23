# MS2 spectrum saving diagnostics (13211.mzML)

During the prior run with `minInt=1e4` and `minPeaks=1`, only 17 MS2 spectra were saved to `ms2_spectra/13211mzML/`, whereas the summary workbook lists 540 unique spectra IDs (6032 rows). This note explains the discrepancy and how to adjust parameters.

## What happened
- **Total MS2 spectra detected:** 540 unique IDs in `13211mzML-ms2Summary.csv` (6032 rows across all entries).
- **Spectra written to CSV:** 17 files in `ms2_spectra/13211mzML/`.

## Filters that remove spectra
The save pipeline only writes a CSV when `ms2_spectrum` returns one or more fitted peaks:
- Spectra with fewer than **4 raw signals** are discarded immediately (`minSignals=4`).
- A peak must exceed **`minInt`**; with `minInt=1e4`, any spectrum whose strongest ion is below 10 000 intensity is skipped.
- After peak fitting, at least **`minPeaks`** peaks must remain (`minPeaks=1` in your run, default is 2). If zero peaks survive, nothing is saved.
- A final **quality filter** keeps peaks with a quality score below `minQuality` (default 100). If all peaks fail this check, the spectrum is dropped.

These checks are implemented in `Functions/ms2_spectrum.py` and used by `Functions/All_ms2_spectra.py` before writing CSV files.

## How to retain more spectra
- Lower `minInt` back to the function default (`1e3` in `All_ms2_spectra`, `1e2` inside `ms2_spectrum`) to keep spectra whose ions are below 10 000 intensity.
- Keep `minPeaks` at least 1 (default 2) but avoid raising it while troubleshooting.
- If your data are sparse, consider reducing `minSignals` to 3 so very small spectra are not dropped outright.
- If you suspect over-filtering by the quality metric, try increasing `minQuality` slightly above 100 to accept more fitted peaks.

After relaxing `minInt` and rerunning, you should see many more CSV files emitted for the same dataset.
