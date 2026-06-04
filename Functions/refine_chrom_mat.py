import numpy as np
def RefineChromMat(ChromatogramMatrix,Chromatogram,ParametersMat,int_col=1,RT_col=0,stdDistance=3,ConstrainPeaks=True):
    IntVec=Chromatogram[:,int_col]
    RT_vec=Chromatogram[:,RT_col]
    ChromatogramMatrix_Adj=ChromatogramMatrix.copy()
    Shape=np.shape(ChromatogramMatrix_Adj)
    Refined_ChromatogramMatrix=np.zeros(Shape)
    NContributions=len(ChromatogramMatrix[0,:])
    SumSubstractVec=np.ones(NContributions)
    RTLoc=np.arange(len(RT_vec))
    ContributionsOrder=ParametersMat[:,2].argsort()
    for peak_id in ContributionsOrder:
        if ConstrainPeaks:
            RT,RT_std=ParametersMat[peak_id,:2]
            min_RT=RT-stdDistance*RT_std
            max_RT=RT+stdDistance*RT_std
            RTLoc=(RT_vec>min_RT)&(RT_vec<max_RT)
        SumSubstractVec[peak_id]=0
        Others_int_Contribution=np.matmul(ChromatogramMatrix_Adj[RTLoc,:],SumSubstractVec)
        SumSubstractVec[peak_id]=1
        Refin_int_Contribution=IntVec[RTLoc]-Others_int_Contribution
        ChromatogramMatrix_Adj[RTLoc,peak_id]=Refin_int_Contribution
    return ChromatogramMatrix_Adj
