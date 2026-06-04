from refine_chrom_peak import *
from mate_generations import *
from evaluate_population import *
from fitness_selector import *
def refine_pop_one_peak(Population,smooth_peaks,boundsMat,NSelect=0,Generations=5):
    Population0=Population.copy()
    NPeaks=len(Population[0])    
    for ParametersMat in Population0:
        NewPopulation=refine_chrom_peak(ParametersMat=ParametersMat,smooth_peaks=smooth_peaks,boundsMat=boundsMat)                
        NewPopulation,r2ListFit=mate_generations(Population=NewPopulation,smooth_peaks=smooth_peaks,Generations=Generations,NSelect=NSelect)                   
        Population=Population+NewPopulation
    r2Vec=evaluate_population(Population=Population,smooth_peaks=smooth_peaks)
    Population,r2ListFit=fitness_selector(r2Vec=r2Vec,Population=Population,NSelect=NSelect) 
    return [Population,r2ListFit]
