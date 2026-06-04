import pandas as pd
from AllSubChromatograms import *
from ResolvingGaussianChromatogram import *
from GaussianParametersTable import *
def ResolveFullChromatogram(mz,mz_std,AllRawPeaks,stdDistance=3,RT_tol=5,minSignals=5,SavePeaks=False,mz_name='-mz'):
    ChromatogramList=AllSubChromatograms(mz=mz,mz_std=mz_std,AllRawPeaks=AllRawPeaks,stdDistance=stdDistance,RT_tol=RT_tol,minSignals=minSignals)
    GaussianParametersList=[]
    for Chromatogram in ChromatogramList:
        GaussianParameters=ResolvingGaussianChromatogram(Chromatogram=Chromatogram,RT_col=2,int_col=1,MaxSignals=100,distance=2)
        if len(GaussianParameters)>0:
            GaussianParametersList.append([GaussianParameters,Chromatogram])
    if SavePeaks:
        GaussianParametersDF=GaussianParametersTable(GaussianParametersList=GaussianParametersList)
        GaussianParametersDF.to_excel(str(mz)+mz_name+'.xlsx')
    return GaussianParametersList
