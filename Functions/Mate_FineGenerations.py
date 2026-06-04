from RefineParametersPopulation import *
from evaluate_population import *
from fitness_selector import *
from mate_square_gauss_par_pop import *
def Mate_FineGenerations(Population,smooth_peaks,boundsMat,Generations=5,NSelect=4):    
    for generation in np.arange(Generations):
        Population=mate_square_gauss_par_pop(SeedPopulation=Population)
        #Population,r2ListFit=Mate_WildGenerations(Population=Population,smooth_peaks=smooth_peaks,Generations=Generations,NSelect=NSelect,boundsMat=boundsMat,NOffspring=50)            
        Population=RefineParametersPopulation(smooth_peaks=smooth_peaks,Population=Population,boundsMat=boundsMat)
        r2Vec=evaluate_population(Population=Population,smooth_peaks=smooth_peaks)
        Population,r2ListFit=fitness_selector(r2Vec=r2Vec,Population=Population,NSelect=NSelect)      
    return [Population,r2ListFit]
