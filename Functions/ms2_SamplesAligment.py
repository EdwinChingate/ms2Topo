import numpy as np
import pandas as pd
import os
import datetime
from JoiningFeatures import *
from ms2_SpectralSimilarityClustering import *
#aligning all ms2 across samples
def ms2_SamplesAligment(ResultsFolder,
                        mz_min = 250,
                        mz_max = 255,
                        RT_min = 0,
                        RT_max = 2000,
                        RT_tol = 30,
                        mz_Tol = 2e-3,
                        min_Int_Frac = 1,
                        cos_tol = 0.8,
                        min_N_ms2_spectra = 3,
                        ToReplace = 'mzML-ms2Summary.xlsx',
                        ms2Folder = 'ms2_spectra',
                        ToAdd = 'mzML',
                        saveAlignedTable = False,
                        name = "SamplesAligment"):
    home = os.getcwd()
    #ResultsFolder = home+'/'+ResultsFolderName
    #replace with a new one for the All_SummMS2
    All_SummMS2Table,SamplesNames = JoiningSummMS2(ResultsFolder = ResultsFolder,
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
                                               min_Int_Frac = min_Int_Frac,
                                               cos_tol = cos_tol)
    N_samples = len(SamplesNames)
    N_Features = len(Modules)
    AlignedSamplesMat = np.zeros((N_Features,N_samples+8))
    AlignedSamples_RT_Mat = np.zeros((N_Features,N_samples+8))
    All_FeaturesTable = All_SummMS2Table
    for feature_id in np.arange(N_Features,dtype = 'int'):
        Feature_module = Modules[feature_id]
        FeatureTable = All_FeaturesTable[Feature_module,:]
        AlignedSamplesMat[feature_id,0] = np.mean(FeatureTable[:,1])
       # AlignedSamplesMat[feature_id,1] = np.std(FeatureTable[:,1])
        #for the confidence interval I need to make a t-student test
        AlignedSamplesMat[feature_id,2] = len(Feature_module)
       # AlignedSamplesMat[feature_id,3] = 7 #CI
       # AlignedSamplesMat[feature_id,4] = 7 #CI
        AlignedSamplesMat[feature_id,5] = np.mean(FeatureTable[:,2])
        AlignedSamplesMat[feature_id,6] = np.min(FeatureTable[:,2])
        AlignedSamplesMat[feature_id,7] = np.max(FeatureTable[:,2])
        Samples_ids = np.array(FeatureTable[:,6],dtype = 'int')
        Samples_ids = set(list(Samples_ids))
        Samples_ids = np.array(list(Samples_ids))
        AlignedSamplesMat_loc = Samples_ids+8
        AlignedSamplesMat[feature_id,AlignedSamplesMat_loc] = 1
        AlignedSamples_RT_Mat[feature_id,AlignedSamplesMat_loc] = 1 #I need to replace with the actual RT
    AlignedSamples_RT_Mat[:,:8] = AlignedSamplesMat[:,:8].copy()
    AlignedSamplesMat = AlignedSamplesMat[AlignedSamplesMat[:,0].argsort()]    
    AlignedSamples_RT_Mat = AlignedSamples_RT_Mat[AlignedSamples_RT_Mat[:,0].argsort()]   
    Columns = ['mz_(Da)','mz_std_(Da)', 'N_ms2-spectra','mz_ConfidenceInterval_(Da)','mz_ConfidenceInterval_(ppm)','RT_(s)','min_RT_(s)','max_RT_(s)']+SamplesNames
    AlignedSamplesDF = pd.DataFrame(AlignedSamplesMat,columns = Columns)
    AlignedSamples_RT_DF = pd.DataFrame(AlignedSamples_RT_Mat,columns = Columns)
    if saveAlignedTable:
        date = datetime.datetime.now()
        string_date = str(date)
        string_date = string_date[:16].replace(':',"_")
        string_date = string_date.replace(' ',"_")
        name = name+"_"+string_date+'.xlsx'
        AlignedSamplesDF.to_excel(name)
        AlignedSamples_RT_DF.to_excel('RT_'+name)
    return [AlignedSamplesDF,AlignedSamples_RT_DF]

