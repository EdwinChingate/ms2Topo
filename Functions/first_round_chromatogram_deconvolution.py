from smooth_data_and_find_peaks import *
from RawGaussParameters import *
from overlapping_gauss_peaks import *
from adjusting_peaks_contributions import *
from updating_chrom_mat import *
from ParametersFitGaussPeaks import *
def first_round_chromatogram_deconvolution(Chromatogram,IntegralFrac=0.1):    
    smooth_peak,peaksMin=smooth_data_and_find_peaks(Chromatogram=Chromatogram)
    ParametersList=RawGaussParameters(smooth_peak=smooth_peak,peaksMin=peaksMin)
    RT_vec=smooth_peak[:,0]
    ChromatogramMatrix=overlapping_gauss_peaks(RT_vec=RT_vec,ParametersList=ParametersList)
    ContributionsVec=adjusting_peaks_contributions(smooth_peak=smooth_peak,ChromatogramMatrix=ChromatogramMatrix)
    Updated_ChromatogramMatrix=updating_chrom_mat(ChromatogramMatrix,ContributionsVec)
    GaussianParList=ParametersFitGaussPeaks(RT_vec=RT_vec,ChromatogramMatrix=Updated_ChromatogramMatrix,ParametersList=ParametersList,minIntegral=minIntegral)
    return GaussianParList
