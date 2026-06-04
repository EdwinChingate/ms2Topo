import numpy as np
def BiggestSelector(r2,r2Vec,Population,lower_std=1e-2):
    BiggestPeakList=[]
    LevelLineVec=np.where(r2Vec==r2)[0]
    if len(LevelLineVec)==1:
        FittestIndividual_id=LevelLineVec[0]
        return FittestIndividual_id
    for Individual_id in LevelLineVec:
        Individual=Population[Individual_id]
        MostIntensePeakInt=np.max(Individual[:,2]/(Individual[:,1]+lower_std))
        BiggestPeakList.append(MostIntensePeakInt)
    if len(BiggestPeakList)==0:
        return -1
    try:
        BiggestPeakVec=np.array(BiggestPeakList)
        BiggestPeak=np.max(BiggestPeakVec)
        BiggestPeakLoc=np.where(BiggestPeakVec==BiggestPeak)[0][0]
    except:
        print(BiggestPeakVec)
    FittestIndividual_id=LevelLineVec[BiggestPeakLoc]
    return FittestIndividual_id
