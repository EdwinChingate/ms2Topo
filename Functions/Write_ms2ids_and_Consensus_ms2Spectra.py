import pandas as pd
import os
import datetime
def Write_ms2ids_and_Consensus_ms2Spectra(feature_id,
                                          feature_module,
                                          consensus_spectraDF,
                                          All_FeaturesTable,
                                          sample_id_col = 6,
                                          ms2_spec_id_col = 0,
                                          explained_Int_col = 2):
    date = datetime.datetime.now()
    string_date = str(date)
    string_date = string_date[:10].replace(':',"_")
    string_date = string_date.replace(' ',"_")
    AligningFolder = 'Alignedms2Features' + string_date
    if not os.path.exists(AligningFolder):
        os.mkdir(AligningFolder)
    FeatureTable = All_FeaturesTable[feature_module, :]
    feature_ms2s_table = FeatureTable[:, [ms2_spec_id_col, sample_id_col, explained_Int_col]]
    feature_ms2sDF = pd.DataFrame(feature_ms2s_table,
                                  columns = ['ms2_id','Sample_id', 'explained_Int(%)']) 
    FeatureClusterLoc = AligningFolder +'/'+str(int(feature_id)) + '.csv'
    feature_ms2sDF.to_csv(FeatureClusterLoc)
    consensus_spectraLoc = AligningFolder +'/Consensus_ms2-spectra_'+str(int(feature_id)) + '.csv' 
    consensus_spectraDF.to_csv(consensus_spectraLoc)
