import numpy as np
from MutateParameters import *
from MutantansExtractor import *
def MutantOffspring(ParametersMat,boundsMat,stdDistance,Mutants=4,mut_stdVec=[0.6,0.7,0.8]):
    NPeaks=len(ParametersMat[:,0])
    NParameters=len(ParametersMat[0,:])
    MutationTensor=np.stack([ParametersMat]*Mutants,axis=0)
    try:
        for parameter_id in np.arange(NParameters):
            boundsVec=boundsMat[parameter_id,:]
            parameter_interval=boundsMat[parameter_id,2]
            mut_std=mut_stdVec[parameter_id]
            ParametersVec=ParametersMat[:,parameter_id]
            MutationTensor[:,:,parameter_id]=MutateParameters(ParametersVec=ParametersVec,boundsVec=boundsVec,parameter_std=mut_std,Mutants=Mutants)
    except:
        show_df(boundsMatRef)
    MutantPopulation=MutantansExtractor(MutationTensor=MutationTensor,Mutants=Mutants)
    return MutantPopulation
