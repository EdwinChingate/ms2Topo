from smooth_fourier import *
from smooth_savgol import *
def SmoothPeak(PeakChr,stdDistance=1,SavgolWindowTimes=2,minPoly=5,int_col=1,RT_col=2):
    smooth_fourier,SavgolWindow_odd=smooth_fourier(PeakChr=PeakChr,stdDistance=stdDistance,SuggestSavgolWindow=True,RT_col=RT_col,int_col=int_col,SavgolWindowTimes=SavgolWindowTimes)
    smooth_savgol=smooth_savgol(PeakChr=smooth_fourier,int_col=1,minWindow=SavgolWindow_odd,minPoly=minPoly)
    return smooth_savgol
