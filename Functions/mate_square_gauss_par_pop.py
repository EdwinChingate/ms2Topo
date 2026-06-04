import numpy as np
def Mate_square_GaussParPop(SeedPopulation):
    NSeedIndividuals=len(SeedPopulation)
    NPeaks=len(SeedPopulation[0])
    Population=[]
    for individual_1 in np.arange(NSeedIndividuals,dtype='int'):
        ParametersMat_i1=SeedPopulation[individual_1]        
        for individual_2 in np.arange(individual_1,NSeedIndividuals,dtype='int'):
            ParametersMat_i2=SeedPopulation[individual_2]
            randomCut_seed=np.random.random()
            randomCut_loc=int(randomCut_seed*(NPeaks-2))+1
            ParametersMat=ParametersMat_i1.copy()
            ParametersMat[randomCut_loc:,:]=ParametersMat_i2[randomCut_loc:,:]
            Population.append(ParametersMat)
    return Population
