from scipy.signal import savgol_filter
def SmoothSavgol(PeakChr,int_col=1,minWindow=11,minPoly=5):
    smooth_savgol=PeakChr.copy()
    NSpec=len(PeakChr[:,int_col])
    wl=min([int(NSpec/4)*2+1,minWindow])
    poly=min([int(wl/3),minPoly])
    SoftInt=savgol_filter(PeakChr[:,int_col], wl, poly)
    smooth_savgol[:,int_col]=SoftInt
    return smooth_savgol
