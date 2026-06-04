from scipy import integrate	
import numpy as np
def GaussBoundaries(smooth_peaks,minValue=1e-5):
    RT_vec=smooth_peaks[:,0]
    Int_vec=smooth_peaks[:,1]
    RT_max=np.max(RT_vec)
    RT_min=np.min(RT_vec)
    RT_maxDif=RT_max-RT_min    
    Integral=integrate.simpson(y=Int_vec,x=RT_vec)
    boundsList=[[RT_min,RT_max,RT_maxDif],[minValue,RT_maxDif,RT_maxDif/6],[minValue,Integral,Integral/2]]
    boundsMat=np.array(boundsList)
    return boundsMat
