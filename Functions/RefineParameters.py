from overlapping_gauss_peaks import *
from refine_chrom_mat import *
from ParametersFitGaussPeaks import *
from adjusting_peaks_contributions import *
from updating_chrom_mat import *
def RefineParameters(ParametersMat,smooth_peaks,boundsMat,ConstrainPeaks=True,keepRTCentroid=True):
    RT_vec=smooth_peaks[:,0]
    ChromatogramMatrix=overlapping_gauss_peaks(RT_vec=RT_vec,ParametersList=ParametersMat,stdDistance=3)
    ContributionsVec=adjusting_peaks_contributions(smooth_peaks=smooth_peaks,ChromatogramMatrix=ChromatogramMatrix)
    ChromatogramMatrix=updating_chrom_mat(ChromatogramMatrix=ChromatogramMatrix,ContributionsVec=ContributionsVec)
    ChromatogramMatrix=refine_chrom_mat(ChromatogramMatrix=ChromatogramMatrix,Chromatogram=smooth_peaks,int_col=1,ParametersMat=ParametersMat,ConstrainPeaks=ConstrainPeaks)
    GaussianParMat=ParametersFitGaussPeaks(RT_vec=RT_vec,ChromatogramMatrix=ChromatogramMatrix,boundsMat=boundsMat,ParametersMat=ParametersMat,keepRTCentroid=keepRTCentroid)        
    return GaussianParMat
