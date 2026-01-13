import numpy as np
import pandas as pd
import os
def Retrieve_csv_ms2Spectra(SummaryFile,ms2Folder,SFindicator='-ms2Summary.xlsx',minQuality=15):
    SummaryFileName=ms2Folder+'/'+SummaryFile
    SummMS2=np.array(pd.read_excel(SummaryFileName,index_col=0))
    ms2FolderName=SummaryFile.replace(SFindicator,'')
    ms2FolderLoc=ms2Folder+'/'+ms2FolderName    
    N_spec=len(SummMS2[:,0])
    SpectraList=[]
    for spectrum_id in np.arange(N_spec,dtype='int'):
        FileName=ms2FolderLoc+'/'+str(spectrum_id)+'.csv'
        Exist=os.path.exists(FileName)
        if Exist:
            spectrum=np.array(pd.read_csv(FileName,index_col=0))
            SpectraList.append(spectrum)
        else:
            SpectraList.append([])
    return [SpectraList,SummMS2]
