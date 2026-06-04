from mate_square_gauss_par_pop import *
from evaluate_population import *
from fitness_selector import *
from MutationTimes import *
def Mate_MutantGenerations(Population,smooth_peaks,boundsMat,mut_stdVec=[0.6,0.7,0.8],Generations=5,NSelect=5,Mutants=5):    
    for generation in np.arange(Generations):
        Population=mate_square_gauss_par_pop(SeedPopulation=Population)
        mut_stdVec=mut_stdVec/(generation*10+1)
        Population=MutationTimes(Population=Population,mut_stdVec=mut_stdVec,boundsMat=boundsMat,Mutants=Mutants)
        r2Vec=evaluate_population(Population=Population,smooth_peaks=smooth_peaks)
        Population,r2ListFit=fitness_selector(r2Vec=r2Vec,Population=Population,NSelect=NSelect) 
    return [Population,r2ListFit]
