from smooth_fourier import *
from smooth_savgol import *
from scipy.signal import find_peaks
def smooth_data_and_find_peaks(Chromatogram,minPoly=3,stdDistance=1,prominence=1,distance=10,MaxSignals=50):
    smooth_fourier,SavgolWindow=smooth_fourier(PeakChr=Chromatogram,stdDistance=stdDistance,SuggestSavgolWindow=True,MaxSignals=MaxSignals)
    smooth_peaks=smooth_savgol(PeakChr=smooth_fourier,int_col=1,minWindow=SavgolWindow,minPoly=minPoly)
    peaksMax=find_peaks(smooth_peaks[:,1],prominence=prominence,distance=distance)[0]
    return [smooth_peaks,peaksMax]
