from RefineChromPeak import *
from Mate_Generations import *
from EvaluatePopulation import *
from FitnessSelector import *
def RefinePop_OnePeak(Population,smooth_peaks,boundsMat,NSelect=0,Generations=5):
    Population0=Population.copy()
    NPeaks=len(Population[0])    
    for ParametersMat in Population0:
        NewPopulation=RefineChromPeak(ParametersMat=ParametersMat,smooth_peaks=smooth_peaks,boundsMat=boundsMat)                
        NewPopulation,r2ListFit=Mate_Generations(Population=NewPopulation,smooth_peaks=smooth_peaks,Generations=Generations,NSelect=NSelect)                   
        Population=Population+NewPopulation
    r2Vec=EvaluatePopulation(Population=Population,smooth_peaks=smooth_peaks)
    Population,r2ListFit=FitnessSelector(r2Vec=r2Vec,Population=Population,NSelect=NSelect) 
    return [Population,r2ListFit]
