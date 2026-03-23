from __future__ import annotations
from ms2_SpectralSimilarityClustering import *

def ms2_SamplesAligment(ProjectName,
                        All_SummMS2Table,
                        EdgesMat,
                        SamplesNames,
                        RT_tol = 30,
                        mz_Tol = 2e-3,
                        feature_id = 0,
                        cos_tol = 0.8,
                        min_N_ms2_spectra = 3,
                        ToReplace = 'mzML-ms2Summary.xlsx',
                        ms2Folder = 'ms2_spectra',
                        ToAdd = 'mzML',
                        Norm2One = True):
                        
    for Low_id_mz, High_id_mz, slice_id in EdgesMat:
        SummMS2_raw = All_SummMS2Table[Low_id_mz: High_id_mz, :]
        AlignedSamplesDF, feature_id = ms2_SpectralSimilarityClustering(SummMS2_raw = SummMS2_raw,
                                                                        SamplesNames = SamplesNames,
                                                                        feature_id = feature_id,
                                                                        slice_id = slice_id,
                                                                        mz_col = 1,
                                                                        RT_col = 2,
                                                                        RT_tol = RT_tol,
                                                                        mz_Tol = mz_Tol,
                                                                        sample_id_col = 6,
                                                                        ms2_spec_id_col = 0,
                                                                        ms2Folder = ms2Folder,
                                                                        ToAdd = ToAdd,
                                                                        cos_tol = cos_tol,
                                                                        Norm2One = Norm2One)     
        TableLoc = ProjectName + '-' + str(slice_id) + '.csv'
        #AlignedSamplesDF.to_csv(TableLoc)
    return AlignedSamplesDF        
    
    
                                                            
