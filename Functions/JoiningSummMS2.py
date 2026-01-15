import pandas as pd
import numpy as np
import os
def JoiningSummMS2(ResultsFolder,
                   mz_min = 0,
                   mz_max = 1200,
                   RT_min = 0,
                   RT_max = 2000,
                   ToReplace = 'mzML-ms2Summary.xlsx'):
    SamplesNames = []
    SamplesList = os.listdir(ResultsFolder)
    SamplesList.sort()
    N_samples = len(SamplesList)
    firstTable = True
    for sample_id in np.arange(N_samples,dtype = 'int'):   
        features_table = SamplesList[sample_id]
        sample_name = features_table.replace(ToReplace,'')
        SamplesNames.append(sample_name)
        features_table_name = ResultsFolder+'/'+features_table
        SummMS2TableDF = pd.read_excel(features_table_name)        
        SummMS2Table = np.array(SummMS2TableDF)
        N_features = len(SummMS2Table[:,0])
        featureLocVec = np.ones(N_features).reshape(-1,1)*sample_id
        SummMS2Table = np.append(SummMS2Table,featureLocVec,axis = 1)
        if firstTable:
            All_SummMS2Table = SummMS2Table
            firstTable = False
        else:
            All_SummMS2Table = np.append(All_SummMS2Table,SummMS2Table,axis = 0)    
    Filter = (All_SummMS2Table[:,1]>mz_min)&(All_SummMS2Table[:,1]<mz_max)&(All_SummMS2Table[:,2]>RT_min)&(All_SummMS2Table[:,2]<RT_max)
    All_SummMS2Table = All_SummMS2Table[Filter,:]
    return [All_SummMS2Table,SamplesNames]

