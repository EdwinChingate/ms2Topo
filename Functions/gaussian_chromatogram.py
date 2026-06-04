from overlapping_gauss_peaks import *
def gaussian_chromatogram(RT_vec,*ParametersList):
    NPeaks=int(len(ParametersList)/3)
    ParametersMat=np.array(ParametersList).reshape(NPeaks, 3)
    ChromatogramMatrix=overlapping_gauss_peaks(RT_vec=RT_vec,ParametersMat=ParametersMat)    
    Int_model=sum(ChromatogramMatrix.T)
    return Int_model
