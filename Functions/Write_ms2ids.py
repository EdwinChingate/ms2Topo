def Write_ms2ids(features_ids,
                 ms2_ids_inModules,
                 AligningFolder = 'Alignedms2Features'):
    #check if the folder exists, then create it 
    for feature_id in features_ids:
        feature_ms2s_table = ms2_ids_inModules[int(feature_id)]
        feature_ms2sDF = pd.DataFrame(feature_ms2s_table,columns = ['ms2_id','Sample_id'])
        FeatureClusterLoc = AligningFolder +'/'+str(feature_id) + '.csv'
        feature_ms2sDF.to_csv(FeatureClusterLoc)
