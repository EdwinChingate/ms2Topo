import numpy as np
import pandas as pd
import os
import datetime
from JoiningSummMS2 import *
#from ms2_SpectralSimilarityClustering import *
#from Write_ms2ids import *
def ms2_SamplesAligment(ResultsFolder,
                        mz_min = 254,
                        mz_max = 255,
                        RT_min = 0,
                        RT_max = 2000,
                        RT_tol = 30,
                        mz_Tol = 2e-3,
                        cos_tol = 0.8,
                        min_N_ms2_spectra = 3,
                        ToReplace = 'mzML-ms2Summary.xlsx',
                        ms2Folder = 'ms2_spectra',
                        ToAdd = 'mzML',
                        saveAlignedTable = False,
                        name = "SamplesAligment",
                        Norm2One = True):
    home = os.getcwd()
    #ResultsFolder = home+'/'+ResultsFolderName
    All_SummMS2Table, SamplesNames = JoiningSummMS2(ResultsFolder = ResultsFolder,
                                                    mz_min = mz_min-3*mz_Tol,
                                                    mz_max = mz_max+3*mz_Tol,
                                                    RT_min = RT_min,
                                                    RT_max = RT_max,
                                                    ToReplace = ToReplace)
    Modules = ms2_SpectralSimilarityClustering(SummMS2_raw = All_SummMS2Table,
                                               SamplesNames = SamplesNames,
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
    Columns = ['mz_(Da)',
               'mz_std_(Da)',
               'N_ms2-spectra',
               'mean CosSim',
               'std CosSim',
               'Normal test',
               'mz_ConfidenceInterval_(Da)',
               'mz_ConfidenceInterval_(ppm)',
               'RT_(s)',
               'min_RT_(s)',
               'max_RT_(s)',
               'feat_id']
    Columns = Columns + SamplesNames 

    #AlignedSamplesDF = pd.DataFrame(AlignedSamplesMat,columns = Columns)
    if saveAlignedTable:
        date = datetime.datetime.now()
        string_date = str(date)
        string_date = string_date[:16].replace(':',"_")
        string_date = string_date.replace(' ',"_")
        name = name+"_"+string_date+'.xlsx'
        AlignedSamplesDF.to_excel(name)
    return AlignedSamplesDF
