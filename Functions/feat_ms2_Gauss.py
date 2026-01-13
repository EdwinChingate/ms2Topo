import numpy as np
from ms2_features_stats import *
def feat_ms2_Gauss(DataSet,
                   SummMS2,
                   MS1IDVec,
                   mz_std=2e-3,
                   MS2_to_MS1_ratio=10,
                   stdDistance=3,
                   MaxCount=3,
                   Points_for_regression=5,
                   minSignals=7):
    MS2_features=[]
    N_MS2_features=len(SummMS2[:,0])
    for MS2_id in np.arange(N_MS2_features,dtype='int'):         
        while True:
            try:
                min_RT=SummMS2[MS2_id,5]
                max_RT=SummMS2[MS2_id,6]
                N_spec=SummMS2[MS2_id,7]
                ms2_spec_id=int(SummMS2[MS2_id,8])
                features_stats=ms2_features_stats(DataSet=DataSet,
                                                  MS2_id=MS2_id,
                                                  SummMS2=SummMS2,
                                                  MS1IDVec=MS1IDVec,
                                                  mz_std=mz_std,
                                                  MS2_to_MS1_ratio=MS2_to_MS1_ratio,
                                                  stdDistance=stdDistance,
                                                  MaxCount=MaxCount,
                                                  Points_for_regression=Points_for_regression,
                                                  minSignals=minSignals)
                if len(features_stats)>0:
                    MS2_features.append(features_stats+[min_RT]+[max_RT]+[N_spec]+[ms2_spec_id])                
                break
            except:
                print('error',MS2_id)
                break
    MS2_features=np.array(MS2_features)
    MS2_features=MS2_features[MS2_features[:,3].argsort(),:]
    columns = ["ms2_id","ms1_id","RT_(s)","mz_(Da)","mz_std_(Da)","I_tot_1spec","Gauss_r2","N_points_1spec","ConfidenceInterval_(Da)","ConfidenceInterval_(ppm)","min_mz_(Da)","max_mz_(Da)","min_RT_(s)","max_RT_(s)","N_ms2_spec","spectra_id"]
    ms2_featuresDF = pd.DataFrame(MS2_features,columns = columns)
    return ms2_featuresDF
