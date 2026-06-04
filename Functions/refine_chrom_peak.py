from overlapping_gauss_peaks import *
from refine_chrom_mat import *
from adjusting_peaks_contributions import *
from updating_chrom_mat import *
from parameters_fit_gauss_parallel_peaks import *
def refine_chrom_peak(ParametersMat,smooth_peaks,boundsMat):
    RT_vec=smooth_peaks[:,0]
    ChromatogramMatrix=overlapping_gauss_peaks(RT_vec=RT_vec,ParametersMat=ParametersMat)  
    ContributionsVec=adjusting_peaks_contributions(smooth_peaks=smooth_peaks,ChromatogramMatrix=ChromatogramMatrix)
    ChromatogramMatrix=updating_chrom_mat(ChromatogramMatrix=ChromatogramMatrix,ContributionsVec=ContributionsVec)    
    ChromatogramMatrix=refine_chrom_mat(ChromatogramMatrix=ChromatogramMatrix,Chromatogram=smooth_peaks,ParametersMat=ParametersMat,int_col=1)
    GaussianPopulation=parameters_fit_gauss_parallel_peaks(RT_vec=RT_vec,ChromatogramMatrix=ChromatogramMatrix,boundsMat=boundsMat,ParametersMat=ParametersMat)    
    return GaussianPopulation
