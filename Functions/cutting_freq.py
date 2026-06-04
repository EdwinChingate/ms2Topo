import numpy as np
from LowSignalClustering import *
def CuttingFreq(fft_signal,frequencies,stdDistance=1,MinSignalFraction=0.5):
    NSig=len(fft_signal)
    NoiseTresVec=LowSignalClustering(SignalVec0=np.abs(fft_signal))[0]
    NoiseTres=NoiseTresVec[2]    
    NoiseLoc=fft_signal<=NoiseTres
    NoiseFreq=frequencies[NoiseLoc]
    Freq_mean=np.mean(abs(NoiseFreq))
    Freq_std=np.std(abs(NoiseFreq))
    FreqTres=Freq_mean-Freq_std*stdDistance
    MinSignalNumber=int(NSig*MinSignalFraction)
    FreqVec=np.abs(frequencies[np.abs(frequencies).argsort()].copy())
    MinFreqTres=FreqVec[MinSignalNumber] 
    FreqTres=np.max([FreqTres,MinFreqTres])
    return FreqTres
