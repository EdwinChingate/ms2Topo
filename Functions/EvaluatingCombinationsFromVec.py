import numpy as np
from OneZero import *
from FitnessSelectorVector import *
from PopulatorFromVec import *
def EvaluatingCombinationsFromVec(SChrom,ParametersMat):
    NPeaks=len(ParametersMat[:,0])
    SelectorVector=np.ones(NPeaks)
    SelectorVectorList=OneZero(SelectorVector=SelectorVector,NPeaks=11,SelectorVectorList=[])
    Int_vec=SChrom[:,1]
    RT_vec=SChrom[:,0]
    r2List=[]
    for SelectorVector in SelectorVectorList:
        Int_model=np.matmul(ChromatogramMatrix,SelectorVector)
        r2=r2_model(RawSignal=Int_vec,ModelSignal=Int_model)
        r2List.append(r2)
    r2Vec=np.array(r2List,dtype='f2')
    FitSelectorVectorList,r2ListFit=FitnessSelectorVector(r2Vec=r2Vec,SelectorVectorList=SelectorVectorList,NSelect=5)
    Population=PopulatorFromVec(ParametersMat=ParametersMat,SelectorVectorList=FitSelectorVectorList)
    return Population
