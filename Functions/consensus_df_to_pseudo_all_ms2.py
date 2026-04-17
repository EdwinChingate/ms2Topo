from __future__ import annotations
import numpy as np

def consensus_df_to_pseudo_all_ms2(consensus_spectra_df,
                                   mz_col = 'median_mz(Da)',
                                   mz_std_col = 'IQR_mz(Da)',
                                   intensity_col = 'mean_Int',
                                   spectrum_id_col = 'feature_id'):

    if consensus_spectra_df is None or len(consensus_spectra_df) == 0:
        return np.array([])

    n_rows = len(consensus_spectra_df)
    pseudo_all_ms2 = np.zeros((n_rows,
                               11))

    pseudo_all_ms2[:, 0] = consensus_spectra_df[mz_col].to_numpy()
    pseudo_all_ms2[:, 1] = consensus_spectra_df[mz_std_col].to_numpy()
    pseudo_all_ms2[:, 9] = consensus_spectra_df[intensity_col].to_numpy()
    pseudo_all_ms2[:, 10] = consensus_spectra_df[spectrum_id_col].astype(int).to_numpy()

    return pseudo_all_ms2




# In[5]: