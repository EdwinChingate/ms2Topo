from resolve_full_chromatogram import *
from RemoveChromBackGround import *
from SplitParametersMat import *
def ResolveChromPeaks(mz,mz_std,AllRawPeaks,stdDistance=3,RT_tol=5,minSignals=5,SavePeaks=False,mz_name='mz',ChromPoints=100,prominence=5,distance=5):
    GaussianParametersList=resolve_full_chromatogram(mz=mz,mz_std=mz_std,AllRawPeaks=AllRawPeaks,stdDistance=stdDistance,RT_tol=RT_tol,minSignals=minSignals,SavePeaks=SavePeaks)
    AllChromPeaks=[]
    for PeakSeed in GaussianParametersList:
        ParametersMat,TresholdList,RT_vec=RemoveChromBackGround(PeakSeed=PeakSeed,stdDistance=stdDistance,ChromPoints=ChromPoints)        
        if len(ParametersMat[:,0])>0:            
            ChromPeaks=SplitParametersMat(RT_vec=RT_vec,ParametersMat=ParametersMat,TresholdList=TresholdList,prominence=prominence,distance=distance,stdDistance=stdDistance)
            AllChromPeaks=AllChromPeaks+ChromPeaks
    if len(AllChromPeaks)==0:
        return []
    AllChromPeaksMat=np.array(AllChromPeaks)
    AllChromPeaksMat=AllChromPeaksMat[AllChromPeaksMat[:,0].argsort(),:]
    return AllChromPeaksMat
