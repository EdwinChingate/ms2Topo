import numpy as np
def ChromGaussPeak(RT_vec,RT,RT_std,Integral,stdDistance=3):
    NSignals=len(RT_vec)
    Gaussian_Int=np.zeros(NSignals)
    min_RT=RT-stdDistance*RT_std
    max_RT=RT+stdDistance*RT_std
    RTLoc=(RT_vec>min_RT)&(RT_vec<max_RT)
    LogVec=-((RT_vec[RTLoc]-RT)/RT_std)**2/2
    f1_sqrt2pi=0.3989422804014327 #1/np.sqrt(np.pi*2) 
    Gaussian_Int[RTLoc]=np.exp(LogVec)*f1_sqrt2pi*Integral/RT_std
    return Gaussian_Int    
