from gaussian_chromatogram import *
def GaussianLambda(RT_vec):
    GaussianLam=lambda loc,*ParametersList: gaussian_chromatogram(loc,RT_vec,*ParametersList)
    return GaussianLam
