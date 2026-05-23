from __future__ import annotations

from pathlib import Path
import pandas as pd
import traceback
from BuildSmallMzML_ForTesting import *

# TODO: unresolved names: x

def BatchBuildSmallMzML_ForTesting(DataFolder,
                                   OutputFolder,
                                   min_mz=0,
                                   max_mz=1200,
                                   min_RT=0,
                                   max_RT=1500,
                                   keep_MS1=True,
                                   min_MS2_peaks=1,
                                   summary_name="SmallMzML_build_summary.csv"):
    """
    Batch version for creating small user-test mzML files.
    """

    DataFolder = Path(DataFolder)
    OutputFolder = Path(OutputFolder)
    OutputFolder.mkdir(parents=True, exist_ok=True)

    dataset_list = sorted([
        x.name for x in DataFolder.iterdir()
        if x.is_file() and x.suffix.lower() == ".mzml"
    ])

    rows = []

    for i, datasetname in enumerate(dataset_list):
        try:
            counts = BuildSmallMzML_ForTesting(
                DataSetName=datasetname,
                DataFolder=DataFolder,
                OutputFolder=OutputFolder,
                OutputFileName=datasetname,
                min_mz=min_mz,
                max_mz=max_mz,
                min_RT=min_RT,
                max_RT=max_RT,
                keep_MS1=keep_MS1,
                min_MS2_peaks=min_MS2_peaks
            )

            counts["status"] = "ok"
            counts["error"] = ""

        except Exception as error:
            counts = {
                "file": datasetname,
                "status": "failed",
                "error": f"{type(error).__name__}: {error}"
            }

            print("\nFAILED:", datasetname, type(error).__name__, error)
            traceback.print_exc(limit=8)

        rows.append(counts)

        print(i + 1, int((i + 1) / max(len(dataset_list), 1) * 100))

    summary_df = pd.DataFrame(rows)
    summary_path = OutputFolder / summary_name
    summary_df.to_csv(summary_path, index=False)

    print(f"\nSummary saved to: {summary_path}")

    return summary_df