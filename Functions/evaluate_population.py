import numpy as np
from r2_Model import *
from OverlappingGaussPeaks import *
def EvaluatePopulation(Population,smooth_peaks):
    NIndividuals=len(Population)
    RT_vec=smooth_peaks[:,0]
    Int_vec=smooth_peaks[:,1]
    r2List=[]
    for individual in np.arange(NIndividuals, dtype='int'):
        ChromatogramMatrix=OverlappingGaussPeaks(RT_vec=RT_vec,ParametersMat=Population[individual])
        Int_model=sum(ChromatogramMatrix.T)
        r2=r2_Model(RawSignal=Int_vec,ModelSignal=Int_model)
        r2List.append(r2)
    r2Vec=np.array(r2List,dtype='f2')
    return r2Vec
