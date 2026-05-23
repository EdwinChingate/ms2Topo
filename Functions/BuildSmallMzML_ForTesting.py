from __future__ import annotations

from pyopenms import MSExperiment
from pyopenms import MzMLFile
from pathlib import Path
from copy_spectrum_with_mz_filtered_peaks import *
from get_n_peaks import *
from get_precursor_mz import *

def BuildSmallMzML_ForTesting(DataSetName,
                              DataFolder,
                              OutputFolder,
                              OutputFileName=None,
                              min_mz=0,
                              max_mz=1200,
                              min_RT=0,
                              max_RT=1500,
                              keep_MS1=True,
                              filter_MS1_peaks=True,
                              keep_empty_MS1=False,
                              min_MS2_peaks=1):
    """
    Builds a small mzML test file while preserving realistic LC-MS/MS structure.

    Keeps:
        - MS1 spectra inside the RT window.
        - For MS1 spectra, optionally removes individual peaks outside
          [min_mz, max_mz].
        - MS2 spectra inside the RT window whose precursor m/z is inside
          [min_mz, max_mz].
        - MS2 fragment peaks are left untouched.

    This creates small test files that still behave like real LC-MS/MS mzML files.
    """

    DataFolder = Path(DataFolder)
    OutputFolder = Path(OutputFolder)
    OutputFolder.mkdir(parents=True, exist_ok=True)

    if OutputFileName is None:
        OutputFileName = DataSetName

    input_path = DataFolder / DataSetName
    output_path = OutputFolder / OutputFileName

    DataSet = MSExperiment()
    MzMLFile().load(str(input_path), DataSet)

    FilteredDataSet = MSExperiment()

    counts = {
        "file": DataSetName,
        "total_spectra_original": 0,
        "ms1_kept": 0,
        "ms1_skipped_empty_after_filter": 0,
        "ms1_peaks_original": 0,
        "ms1_peaks_kept": 0,
        "ms2_kept": 0,
        "ms2_skipped_no_precursor": 0,
        "ms2_skipped_mz": 0,
        "ms2_skipped_rt": 0,
        "ms2_skipped_few_peaks": 0,
        "output_path": str(output_path)
    }

    for spectrum in DataSet:
        counts["total_spectra_original"] += 1

        ms_level = spectrum.getMSLevel()
        rt = spectrum.getRT()

        if rt < min_RT or rt > max_RT:
            if ms_level == 2:
                counts["ms2_skipped_rt"] += 1
            continue

        if ms_level == 1:
            if not keep_MS1:
                continue

            if filter_MS1_peaks:
                original_n_peaks = get_n_peaks(spectrum)

                filtered_spectrum = copy_spectrum_with_mz_filtered_peaks(
                    spectrum=spectrum,
                    min_mz=min_mz,
                    max_mz=max_mz
                )

                filtered_n_peaks = get_n_peaks(filtered_spectrum)

                counts["ms1_peaks_original"] += original_n_peaks
                counts["ms1_peaks_kept"] += filtered_n_peaks

                if filtered_n_peaks == 0 and not keep_empty_MS1:
                    counts["ms1_skipped_empty_after_filter"] += 1
                    continue

                FilteredDataSet.addSpectrum(filtered_spectrum)

            else:
                counts["ms1_peaks_original"] += get_n_peaks(spectrum)
                counts["ms1_peaks_kept"] += get_n_peaks(spectrum)
                FilteredDataSet.addSpectrum(spectrum)

            counts["ms1_kept"] += 1
            continue

        if ms_level != 2:
            continue

        precursor_mz = get_precursor_mz(spectrum)

        if precursor_mz is None:
            counts["ms2_skipped_no_precursor"] += 1
            continue

        if precursor_mz < min_mz or precursor_mz > max_mz:
            counts["ms2_skipped_mz"] += 1
            continue

        n_peaks = get_n_peaks(spectrum)

        if n_peaks < min_MS2_peaks:
            counts["ms2_skipped_few_peaks"] += 1
            continue

        # Important: MS2 fragment peaks are not filtered by precursor m/z interval.
        FilteredDataSet.addSpectrum(spectrum)
        counts["ms2_kept"] += 1

    MzMLFile().store(str(output_path), FilteredDataSet)

    print(f"Saved: {output_path}")
    print(f"MS1 spectra kept: {counts['ms1_kept']}")
    print(f"MS1 peaks kept: {counts['ms1_peaks_kept']} / {counts['ms1_peaks_original']}")
    print(f"MS2 spectra kept: {counts['ms2_kept']}")

    return counts