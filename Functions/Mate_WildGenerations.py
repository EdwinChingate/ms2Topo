from Mate_square_WildPop import *
from evaluate_population import *
from fitness_selector import *
def Mate_WildGenerations(Population,smooth_peaks,boundsMat,Generations=5,NSelect=10,NOffspring=10):    
    for generation in np.arange(Generations):
        Population=Mate_square_WildPop(SeedPopulation=Population,boundsMat=boundsMat,NOffspring=NOffspring) 
        r2Vec=evaluate_population(Population=Population,smooth_peaks=smooth_peaks)        
        Population,r2ListFit=fitness_selector(r2Vec=r2Vec,Population=Population,NSelect=NSelect) 
    return [Population,r2ListFit]
