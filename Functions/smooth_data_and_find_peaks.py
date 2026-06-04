from SmoothFourier import *
from SmoothSavgol import *
from scipy.signal import find_peaks
def SmoothData_and_FindPeaks(Chromatogram,minPoly=3,stdDistance=1,prominence=1,distance=10,MaxSignals=50):
    smooth_fourier,SavgolWindow=SmoothFourier(PeakChr=Chromatogram,stdDistance=stdDistance,SuggestSavgolWindow=True,MaxSignals=MaxSignals)
    smooth_peaks=SmoothSavgol(PeakChr=smooth_fourier,int_col=1,minWindow=SavgolWindow,minPoly=minPoly)
    peaksMax=find_peaks(smooth_peaks[:,1],prominence=prominence,distance=distance)[0]
    return [smooth_peaks,peaksMax]
