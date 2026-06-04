import numpy as np
from umbrellas_stats import *
import random
from refine_pop_one_peak import *
from fitness_selector import *
def raw_gauss_seed(smooth_peaks,peaksMax,boundsMat,NSelect=5,Generations=5,minContribution=2):
    NPeaks=len(peaksMax)
    NSignals=int(len(smooth_peaks[:,0]))
    PeaksUmbrellaMat=np.zeros((NPeaks,6))
    PeaksUmbrellaMat[:,0]=peaksMax
    PeakValley=np.array((peaksMax[1:]+peaksMax[:-1])/2,dtype='int')
    PeaksUmbrellaMat[1:,1]=PeakValley
    PeaksUmbrellaMat[:-1,2]=PeakValley
    PeaksUmbrellaMat[-1,2]=NSignals
    PeaksUmbrellaMat=umbrellas_stats(smooth_peaks=smooth_peaks,PeaksUmbrellaMat=PeaksUmbrellaMat,NPeaks=NPeaks)
    ParametersMat=PeaksUmbrellaMat[:,3:]    
    ExtraPeak=(np.mean(ParametersMat,axis=0)).reshape(1,-1)+random.random()
    ParametersMat=np.append(ParametersMat,ExtraPeak,axis=0)
    ExtraPeak=(np.median(ParametersMat,axis=0)).reshape(1,-1)
    ParametersMat=np.append(ParametersMat,ExtraPeak,axis=0)
    ParametersMat=ParametersMat[ParametersMat[:,0].argsort(),:]    
    Population,r2ListFit=refine_pop_one_peak(Population=[ParametersMat],smooth_peaks=smooth_peaks,boundsMat=boundsMat,NSelect=NSelect,Generations=Generations)
    Population,r2ListFit=fitness_selector(r2Vec=r2ListFit,Population=Population,NSelect=1)     
    ParametersMat=Population[0]
    Integral=boundsMat[2,1]
    minIntegralContribution=Integral*minContribution/100        
    ContributionFilter=ParametersMat[:,2]>minIntegralContribution
    ParametersMat=ParametersMat[ContributionFilter,:] 
    return ParametersMat
