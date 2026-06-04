import numpy as np
from BiggestSelector import *
def FitnessSelector(r2Vec,Population,NSelect=0):
    if NSelect==0:
        NSelect=len(Population)
    FitPopulation=[]
    r2Vec_unique=np.array(list(set(r2Vec.copy())))
    Sortr2Vec=(-r2Vec_unique).argsort()  
    r2Vec_unique=r2Vec_unique[Sortr2Vec]
    r2ListFit=[]
    for r2 in r2Vec_unique:
        FittestIndividual_id=BiggestSelector(r2=r2,r2Vec=r2Vec,Population=Population)
        if FittestIndividual_id>=0:
            FittestIndividual=Population[FittestIndividual_id]
            FitPopulation.append(Population[FittestIndividual_id])
            r2ListFit.append(r2Vec[FittestIndividual_id])   
        if len(FitPopulation)==NSelect:
            break
    return [FitPopulation,r2ListFit]
