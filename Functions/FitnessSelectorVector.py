import numpy as np
from biggest_selector import *
def FitnessSelectorVector(r2Vec,SelectorVectorList,NSelect=0):
    if NSelect==0:
        NSelect=len(SelectorVectorList)
    FitPopulation=[]
    r2Vec_unique=np.array(list(set(r2Vec.copy())))
    Sortr2Vec=(-r2Vec_unique).argsort()  
    r2Vec_unique=r2Vec_unique[Sortr2Vec]
    r2ListFit=[]
    for r2 in r2Vec_unique:
        FittestIndividual_id=np.where(r2Vec==r2)[0][0]
        FittestIndividual=SelectorVectorList[FittestIndividual_id]
        FitPopulation.append(FittestIndividual)
        r2ListFit.append(r2Vec[FittestIndividual_id])   
        if len(FitPopulation)==NSelect:
            break
    return [FitPopulation,r2ListFit]
