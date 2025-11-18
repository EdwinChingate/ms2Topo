import numpy as np
import pandas as pd
import os
from ChargeDataSet import *
from MS_L_IDs import *
from Match_Feature_O2O_Chrom import *
def Refine_O2O_FeaturesTable_withChromatogram(AlignedSamplesDFName,FirstSample=4,mz_tol=5,RT_tol=5):
    AlignedSamplesDF=pd.read_excel(AlignedSamplesDFName,index_col=0)
    AlignedSamplesDF_RT=AlignedSamplesDF.copy()
    Sample_IDs=list(AlignedSamplesDF.columns)[FirstSample:]
    for sample_id in Sample_IDs:
        DataSetName=sample_id.replace('.xlsx','.mzML')
        PathExist=os.path.exists('Data\\'+DataSetName)
        if PathExist:     
            print('Existing file: '+DataSetName)
            DataSet=ChargeDataSet(DataSetName,OSLinux=False)
            MS1IDVec=MS_L_IDs(DataSet=DataSet,Level=1,min_RT=0,max_RT=2500)
            FeaturesIds=list(AlignedSamplesDF.index)    
            for ms2_feature_id in FeaturesIds:  
                try:
                    Closest_RT,ChosenPeakInt=Match_Feature_O2O_Chrom(AlignedSamplesDF=AlignedSamplesDF,MS1IDVec=MS1IDVec,DataSet=DataSet,ms2_feature_id=ms2_feature_id,RT_tol=5,mz_Tol=1,RT_window=30)
                except:
                    print('Error with feature: ',ms2_feature_id)
                    Closest_RT,ChosenPeakInt=[0,0]
                AlignedSamplesDF[sample_id][ms2_feature_id]=ChosenPeakInt/60
                AlignedSamplesDF_RT[sample_id][ms2_feature_id]=Closest_RT/60
        else:
            print('Missing file: '+DataSetName)
    AlignedSamplesDF.to_excel(AlignedSamplesDFName)
    AlignedSamplesDF_RT.to_excel('RT_'+AlignedSamplesDFName)
    return AlignedSamplesDF
