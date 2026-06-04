import numpy as np
from CuttingFreq import *
from RedistributeSampling import *
def SmoothFourier(PeakChr,stdDistance=1,RT_col=2,int_col=1,SuggestSavgolWindow=False,SavgolWindowTimes=2,MaxSignals=50):
    N_signals=len(PeakChr[:,RT_col])
    RedisPeak=RedistributeSampling(PeakChr=PeakChr,RT_col=RT_col,int_col=int_col)
    time=RedisPeak[:,0]
    signal=RedisPeak[:,1]
    NSig=len(signal)
    min_RT=np.min(time)
    max_RT=np.max(time)
    RT_total=max_RT-min_RT
    SamplingRate=N_signals/RT_total
    fft_signal=np.fft.fft(signal)
    frequencies = np.fft.fftfreq(NSig,d=(time[1] - time[0]))    
    FreqTres=CuttingFreq(fft_signal=fft_signal,frequencies=frequencies,stdDistance=stdDistance,MinSignalFraction=0.5)
    fft_filtered=fft_signal.copy()
    fft_filtered[np.abs(frequencies)>FreqTres] = 0
    filtered_signal = np.fft.ifft(fft_filtered).real
    smooth_fourier=RedisPeak.copy()
    smooth_fourier[:,1]=np.abs(filtered_signal)  
    N_signals=np.min([N_signals,MaxSignals])
    smooth_fourier=RedistributeSampling(PeakChr=smooth_fourier,N_new=N_signals,RT_col=0,int_col=1)
    if SuggestSavgolWindow:
        SavgolWindow=SamplingRate/FreqTres*SavgolWindowTimes
        SavgolWindow_odd=int(SavgolWindow/2)*2+1
        return [smooth_fourier,SavgolWindow_odd]
    return smooth_fourier
