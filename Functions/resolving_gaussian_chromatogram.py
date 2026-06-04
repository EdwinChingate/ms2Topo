from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from gaussian_chromatogram import *
from tools_gaussian_chrom import *
from show_df import *
def resolving_gaussian_chromatogram(Chromatogram,RT_col=2,int_col=1,MaxSignals=100,distance=2,ShowErrorChrom=False):
    SChrom,ParametersList,bounds=tools_gaussian_chrom(Chromatogram=Chromatogram,RT_col=RT_col,int_col=int_col,MaxSignals=MaxSignals,distance=distance)
    if len(SChrom)==0:
        return []
    RT_vec=SChrom[:,0]
    Int_vec=SChrom[:,1]
    try:
        GaussianParametersList=list(curve_fit(gaussian_chromatogram, xdata=RT_vec, ydata=Int_vec,p0=ParametersList,bounds=bounds)[0])
        NPeaks=int(len(GaussianParametersList)/3)
        GaussianParameters=np.array(GaussianParametersList).reshape(NPeaks, 3)
        GaussianParameters=GaussianParameters[GaussianParameters[:,0].argsort(),:]
        return GaussianParameters
    except:
        if ShowErrorChrom:
            show_df(ParametersList)
            plt.plot(Chromatogram[:,RT_col],Chromatogram[:,int_col],'.')
            plt.show()
        return []
