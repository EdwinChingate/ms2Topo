from MaxIntChromatogram import *
from Feat_RT_edges import *
from BaseLine import *
from show_df import *
import matplotlib.pyplot as plt
def PlotChromatogram(mz,mz_std,DataSet,DataSetName,MS1IDVec,AllPeaks,minIntFrac=1,int_col=1,RT_col=2,BaseLinePoints_2=3,LogFileName='LogFile_ms1.csv',stdDistance=1,minSignals=5,MaxCount=3,minInt=1e3,Points_for_regression=4,alpha=0.01,minSpec=10,minWindow=11,minPoly=5):
    Chromatogram=MaxIntChromatogram(mz=mz,mz_std=mz_std,AllPeaks=AllPeaks,stdDistance=stdDistance)    
    Chromatogram=Chromatogram[Chromatogram[:,RT_col].argsort(),:].copy()
    ChrMat=Feat_RT_edges(Chromatogram=Chromatogram,minSpec=minSpec,int_col=int_col,stdDistance=3,NoiseCluster=False)
    plt.plot(Chromatogram[:,2],Chromatogram[:,1],'.')
    plt.show()
    show_df(ChrMat)
    if len(ChrMat)==0:
        return []
    min_mz=mz-mz_std*stdDistance
    max_mz=mz+mz_std*stdDistance
    SummarizeChFeat=[]
    for sig in ChrMat:
        EarlyLoc=int(sig[0])
        LateLoc=int(sig[1])
        PeakChr=Chromatogram[EarlyLoc:LateLoc,:]    
        NSpec=len(PeakChr[:,0])
        wl=min([int(NSpec/4)*2+1,minWindow])
        poly=min([int(wl/2),minPoly])    
        SoftInt=savgol_filter(PeakChr[:,int_col], wl, poly)
        BL=BaseLine(EarlyLoc=EarlyLoc,LateLoc=LateLoc,Chromatogram=Chromatogram,RT_col=RT_col,int_col=int_col,BaseLinePoints_2=BaseLinePoints_2)
        No_NoiseSignal=SoftInt-BL
        plt.plot(PeakChr[:,2],PeakChr[:,1],'.')
        plt.plot(PeakChr[:,2],SoftInt,'-')
        plt.plot(PeakChr[:,2],BL,'-')
        plt.show()
        maxInt=np.max(No_NoiseSignal)
        minInt=minIntFrac*maxInt/100
        PosLoc=np.where(No_NoiseSignal>minInt)[0]
        if len(PosLoc)<4:
            return 0
        No_NoiseSignal=No_NoiseSignal[PosLoc]
        X=PeakChr[PosLoc,RT_col]
        Y=No_NoiseSignal
        plt.plot(X,Y,'-')
        plt.show()
    return Chromatogram
