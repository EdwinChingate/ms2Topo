from __future__ import annotations

from pathlib import Path
import pandas as pd

def JoinCSVFilesInFolder(folder_path,
                         add_source_file = True,
                         file_pattern = "*.csv",
                         encoding = "utf-8"):
    """
    Read all CSV files in a folder and concatenate them into one DataFrame.

    The function assumes that the CSV files have compatible columns. When
    add_source_file is True, a source_file column is added so each row can be
    traced back to the file it came from.
    """

    folder_path = Path(folder_path)

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")

    csv_files = sorted(folder_path.glob(file_pattern))

    if len(csv_files) == 0:
        raise FileNotFoundError(f"No CSV files found in: {folder_path}")

    dataframe_list = []

    for csv_file in csv_files:
        current_df = pd.read_csv(csv_file,
                                 encoding = encoding,
                                 index_col = 0)

        if add_source_file:
            current_df["source_file"] = csv_file.name

        dataframe_list.append(current_df)

    joined_df = pd.concat(dataframe_list,
                          axis = 0,
                          ignore_index = True)
    joined_df = joined_df.sort_values(by = 'median_mz(Da)',
                                      ascending=False)

    return joined_df
    
from __future__ import annotations